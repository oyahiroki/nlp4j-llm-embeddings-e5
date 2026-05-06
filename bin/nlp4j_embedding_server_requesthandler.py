# coding: utf-8

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import json
import traceback
import time
import datetime
from sentence_transformers import SentenceTransformer, util


# ===== Model init (once) =====
print("initializing ... 1/2")
model = SentenceTransformer('intfloat/multilingual-e5-large')
print("initializing ... 2/2")
model.encode(["test"], normalize_embeddings=True)
print("initializing ... done")


# ===== E5 prefix helpers =====
def _ensure_passage_prefix(text: str) -> str:
	# 文書側 prefix
	if text is None:
		return ""
	if text.startswith("passage:"):
		return text
	return "passage: " + text


def _ensure_query_prefix(text: str) -> str:
	# クエリ側 prefix
	if text is None:
		return ""
	if text.startswith("query:"):
		return text
	return "query: " + text


# ===== token helpers =====
def _is_true(v) -> bool:
	"""
	'true' / 'True' / True / ['true'] などを True 扱いにする
	"""
	if v is None:
		return False
	if isinstance(v, list):
		if len(v) == 0:
			return False
		v = v[0]
	return str(v).lower() == "true"


def _count_tokens(text: str) -> int:
	"""
	SentenceTransformer の tokenizer を用いて token 数を数える。
	truncation=False なので「切り捨てずに」数える。
	"""
	tokenizer = getattr(model, "tokenizer", None)
	if tokenizer is None:
		return 0

	encoded = tokenizer(
		text,
		truncation=False,
		add_special_tokens=True,
		return_attention_mask=False,
		return_token_type_ids=False
	)
	return len(encoded["input_ids"])


def _get_max_tokens() -> int:
	tokenizer = getattr(model, "tokenizer", None)
	if tokenizer is None:
		return 512
	max_len = getattr(tokenizer, "model_max_length", 512)
	# HuggingFace では model_max_length が巨大値扱いのときがあるので保険
	if max_len is None or max_len > 100000:
		return 512
	return int(max_len)


def _warn_if_truncated(label: str, token_count: int, max_tokens: int):
	if token_count > max_tokens:
		print(f"[WARN][TOKEN_LIMIT]{label} token_count={token_count} max_tokens={max_tokens} truncated=True")


class EmbeddingRequestHandler(BaseHTTPRequestHandler):
	count = 0

	def log_message(self, format, *args):
		# quiet
		pass

	# ---- /embeddings (document embedding for search; E5 passage prefix) ----
	def embeddings(self, text, checktokencount: bool = False):
		EmbeddingRequestHandler.count += 1
		try:
			original_text = "" if text is None else text
			e5_text = _ensure_passage_prefix(original_text)

			res = {
				"message": "ok",
				"time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
				"text": original_text
			}

			if checktokencount:
				token_count = _count_tokens(e5_text)
				max_tokens = _get_max_tokens()
				res["token_count"] = token_count
				res["max_tokens"] = max_tokens
				truncated = (token_count > max_tokens)
				res["truncated"] = truncated
				if truncated:
					_warn_if_truncated(label="[/embeddings][PASSAGE]", token_count=token_count, max_tokens=max_tokens)

			embed_start_time = time.time()
			embeddings = model.encode([e5_text], normalize_embeddings=True)
			embed_end_time = time.time()

			res["embeddings"] = embeddings.tolist()[0]

			self.send_response(200)
			self.send_header("Content-type", "application/json; charset=utf-8")
			self.end_headers()
			self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
			self.close_connection = True

			print("Embedding Time: {:.6f} seconds".format(embed_end_time - embed_start_time))

		except Exception:
			print(traceback.format_exc())
			self.send_response(500)

	# ---- /semantic_search (query + corpus; E5 query/passage prefixes) ----
	def semantic_search(self, text, texts, checktokencount: bool = False):
		EmbeddingRequestHandler.count += 1
		try:
			query_original = "" if text is None else text
			query_e5 = _ensure_query_prefix(query_original)

			res = {
				"message": "ok",
				"time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
				"text": query_original
			}

			# GET: text2 で 1件コーパスが来る / POST: texts(list) が来る、両方に対応
			if texts is None:
				corpus_list = []
			elif isinstance(texts, str):
				corpus_list = [texts]
			else:
				corpus_list = texts

			corpus_e5 = [_ensure_passage_prefix("" if t is None else t) for t in corpus_list]

			if checktokencount:
				q_tc = _count_tokens(query_e5)
				max_tokens = _get_max_tokens()
				res["query_token_count"] = q_tc
				res["max_tokens"] = max_tokens
				query_truncated = (q_tc > max_tokens)
				res["query_truncated"] = query_truncated
				if query_truncated:
					_warn_if_truncated(label="[/semantic_search][QUERY]", token_count=q_tc, max_tokens=max_tokens)

				# コーパスの token 数を全件数えると重いので件数のみ返す
				res["corpus_size"] = len(corpus_e5)

			embed_start_time = time.time()

			if len(corpus_e5) == 0:
				r = [[]]
			else:
				query_embedding = model.encode([query_e5], normalize_embeddings=True)[0]
				corpus_embeddings = model.encode(corpus_e5, normalize_embeddings=True)
				r = util.semantic_search(query_embedding, corpus_embeddings)

			embed_end_time = time.time()

			res["r"] = r[0]

			self.send_response(200)
			self.send_header("Content-type", "application/json; charset=utf-8")
			self.end_headers()
			self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
			self.close_connection = True

			print("Embedding Time: {:.6f} seconds".format(embed_end_time - embed_start_time))

		except Exception:
			print(traceback.format_exc())
			self.send_response(500)

	# ---- /cos_sim (no prefix by default; optional token count) ----
	def cos_sim(self, text1, text2, checktokencount: bool = False):
		EmbeddingRequestHandler.count += 1
		try:
			embed_start_time = time.time()

			t1 = "" if text1 is None else text1
			t2 = "" if text2 is None else text2

			response_data = {'text1': t1, 'text2': t2}

			if checktokencount:
				max_tokens = _get_max_tokens()
				tc1 = _count_tokens(t1)
				tc2 = _count_tokens(t2)
				response_data['max_tokens'] = max_tokens
				response_data['token_count1'] = tc1
				response_data['token_count2'] = tc2
				truncated1 = (tc1 > max_tokens)
				truncated2 = (tc2 > max_tokens)
				response_data['truncated1'] = truncated1
				response_data['truncated2'] = truncated2

				if truncated1:
					_warn_if_truncated(label="[/cos_sim][TEXT1]", token_count=tc1, max_tokens=max_tokens)
				if truncated2:
					_warn_if_truncated(label="[/cos_sim][TEXT2]", token_count=tc2, max_tokens=max_tokens)

			ee = model.encode([t1, t2], normalize_embeddings=True)
			r = util.cos_sim(ee[0], ee[1])
			response_data['cosine_similarity'] = r.item()

			self.send_response(200)
			self.send_header("Content-type", "application/json; charset=utf-8")
			self.end_headers()
			self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
			self.close_connection = True

			embed_end_time = time.time()
			print("2 Embeddings Time: {:.6f} seconds".format(embed_end_time - embed_start_time))

		except KeyboardInterrupt:
			print("catch on main")
			raise
		except Exception as e:
			print(e)
			self.send_response(500)
			self.send_header('Content-type', 'application/json; charset=utf-8')
			self.end_headers()
			self.wfile.write(json.dumps({}).encode('utf-8'))

	def do_POST(self):
		parsed_path = urlparse(self.path)
		path = parsed_path.path
		content_length = int(self.headers.get('content-length', '0'))
		request_body = json.loads(self.rfile.read(content_length).decode('utf-8')) if content_length > 0 else {}

		checktokencount = _is_true(request_body.get("checktokencount"))

		if path == '/cos_sim':
			text1 = request_body.get('text1')
			text2 = request_body.get('text2')
			self.cos_sim(text1, text2, checktokencount)
			return

		elif path == '/embeddings':
			text = request_body.get('text')
			self.embeddings(text, checktokencount)
			return

		elif path == '/semantic_search':
			text = request_body.get('text')
			texts = request_body.get('texts')
			self.semantic_search(text, texts, checktokencount)
			return

		else:
			text = request_body.get('text')
			self.embeddings(text, checktokencount)
			return

	def do_GET(self):
		parsed_path = urlparse(self.path)
		path = parsed_path.path
		qs_d = parse_qs(parsed_path.query)

		checktokencount = _is_true(qs_d.get("checktokencount"))

		if path == '/semantic_search':
			# 互換：text1, text2
			if "text1" not in qs_d or "text2" not in qs_d:
				self.send_response(404)
				self.end_headers()
				return
			text1 = unquote(qs_d["text1"][0])
			text2 = unquote(qs_d["text2"][0])
			self.semantic_search(text1, text2, checktokencount)
			return

		elif path == '/cos_sim':
			if "text1" not in qs_d or "text2" not in qs_d:
				self.send_response(404)
				self.end_headers()
				return
			text1 = unquote(qs_d["text1"][0])
			text2 = unquote(qs_d["text2"][0])
			self.cos_sim(text1, text2, checktokencount)
			return

		elif path == '/embeddings':
			if "text" not in qs_d:
				self.send_response(404)
				self.end_headers()
				return
			text = unquote(qs_d["text"][0])
			self.embeddings(text, checktokencount)
			return

		else:
			# qs なしなら index.html を返す
			if not qs_d:
				self.send_response(200)
				self.send_header("Content-type", "text/html; charset=utf-8")
				self.end_headers()
				with open('html/index.html', 'r', encoding='utf-8') as file:
					self.wfile.write(file.read().encode('utf-8'))
				return

			# qs がある場合は embeddings にフォールバック
			if "text" not in qs_d:
				self.send_response(404)
				self.end_headers()
				return
			text = unquote(qs_d["text"][0])
			self.embeddings(text, checktokencount)
			return
