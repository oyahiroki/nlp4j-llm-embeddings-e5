# coding: utf-8

# /embedding Embedding Server
# /semanticsearch Semantic Search Server
# / (default) Embedding Server

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import json
import traceback
from socketserver import ThreadingMixIn
import sys
import time
import datetime
import signal
from sentence_transformers import SentenceTransformer, util
import argparse


print("initializing ... 1/2")
model = SentenceTransformer('intfloat/multilingual-e5-large')  # モデルの一度きりの初期化
print("initializing ... 2/2")
model.encode(["test"])
print("initializing ... done")

class EmbeddingRequestHandler(BaseHTTPRequestHandler):
	count = 0

	def log_message(self, format, *args):
		pass
	
	def embeddings(self, text):
		EmbeddingRequestHandler.count += 1
		try:
			res = {"message": "ok", "time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "text": text}
			sentences = [text]
			
			# Embedding処理の時間計測開始
			embed_start_time = time.time()
			embeddings = model.encode(sentences)  # グローバルモデル変数を使用
			embed_end_time = time.time()
			# Embedding処理の時間計測終了
			
			res["embeddings"] = embeddings.tolist()[0]

			self.send_response(200)
			self.send_header("Content-type", "application/json; charset=utf-8")
			self.end_headers()
			html = json.dumps(res)
			self.wfile.write(html.encode())
			self.close_connection = True

			# 処理時間の出力
			print("Embedding Time: {:.6f} seconds".format(embed_end_time - embed_start_time))
			
			del html, res
		except Exception as e:
			print(traceback.format_exc())
			self.send_response(500)
	
	# クエリと最も意味的に類似しているテキストのインデックスと類似度スコアを含む結果のリストを返します
	def semantic_search(self, text, texts):
		EmbeddingRequestHandler.count += 1
		try:
			res = {"message": "ok", "time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "text": text}
			sentences = [text]
			
			# Embedding処理の時間計測開始
			embed_start_time = time.time()
			# embedding (1)
			query_embedding = model.encode(text)
			# embedding (2)
			corpus_embeddings = model.encode(texts)
			# semantic search
			r = util.semantic_search(query_embedding, corpus_embeddings)
			embed_end_time = time.time()
			# Embedding処理の時間計測終了
			
			res["r"] = r[0]

			self.send_response(200)
			self.send_header("Content-type", "application/json; charset=utf-8")
			self.end_headers()
			html = json.dumps(res)
			self.wfile.write(html.encode())
			self.close_connection = True

			# 処理時間の出力
			print("Embedding Time: {:.6f} seconds".format(embed_end_time - embed_start_time))
			
			del html, res
		except Exception as e:
			print(traceback.format_exc())
			self.send_response(500)
			
	# 二つのベクトル間のコサイン類似度を計算します
	def cos_sim(self, text1, text2):
		EmbeddingRequestHandler.count += 1
		try:
			embed_start_time = time.time()
			ee = model.encode([text1,text2])
			r = util.cos_sim(ee[0],ee[1])
			response_data = {'text1':text1,'text2':text2, 'cosine_similarity':r.item()}
			response_json = json.dumps(response_data).encode('utf-8')
			self.send_response(200)
			self.send_header("Content-type","application/json; charset=utf-8")
			self.end_headers()
			self.wfile.write(response_json)
			self.close_connection = True
			embed_end_time = time.time()
			# 処理時間の出力
			print("2 Embeddings Time: {:.6f} seconds".format(embed_end_time - embed_start_time))
			del response_json
			del response_data
		except KeyboardInterrupt:
			print("catch on main")
			raise
		except Exception as e:
			print(e)
			self.send_response(500)
			self.send_header('Content-type','application/json')
			self.end_headers()
			response = {}
			responsebody = json.dumps(response)
			self.wfile.write(responsebody.encode('utf-8'))
	
	def do_POST(self):
		parsed_path = urlparse(self.path)
		path = parsed_path.path
		content_length = int(self.headers.get('content-length'))
		request_body = json.loads(self.rfile.read(content_length).decode('utf-8'))
		
		if path == '/cos_sim':
			text1 = request_body.get('text1')
			text2 = request_body.get('text2')
			self.cos_sim(text1,text2)
			return
		elif path == '/embeddings':
			text = request_body.get('text')
			self.embeddings(text)
			return
		elif path == '/semantic_search':
			text = request_body.get('text')
			texts = request_body.get('texts')
			self.semantic_search(text,texts)
			return
		else:
			text = request_body.get('text')
			self.embeddings(text)
			return
	
	def do_GET(self):
		parsed_path = urlparse(self.path)
		path = parsed_path.path
		# print("path: " + path)
		query = parsed_path.query
		qs_d = parse_qs(query)
		if path == '/semantic_search':
			if "text1" not in qs_d:
				self.send_response(404)
				self.end_headers()
				return
			if "text2" not in qs_d:
				self.send_response(404)
				self.end_headers()
				return
			text1 = qs_d["text1"][0]
			text1 = unquote(text1)
			text2 = qs_d["text2"][0]
			text2 = unquote(text2)
			self.semantic_search(text1,text2)
			return
		elif path == '/cos_sim':
			if "text1" not in qs_d:
				self.send_response(404)
				self.end_headers()
				return
			if "text2" not in qs_d:
				self.send_response(404)
				self.end_headers()
				return
			text1 = qs_d["text1"][0]
			text1 = unquote(text1)
			text2 = qs_d["text2"][0]
			text2 = unquote(text2)
			self.cos_sim(text1,text2)
			return
		elif path == '/embeddings':
			if "text" not in qs_d:
				self.send_response(404)
				self.end_headers()
				return
			text = qs_d["text"][0]
			text = unquote(text)
			self.embeddings(text)
			return
		else:
			
			if not qs_d:
				self.send_response(200)
				self.send_header("Content-type", "text/html; charset=utf-8")
				self.end_headers()
				with open('html/index.html', 'r', encoding='utf-8') as file:
					html_content = file.read()
					self.wfile.write(html_content.encode('utf-8'))
			else:
				if "text" not in qs_d:
					self.send_response(404)
					self.end_headers()
					return
				text = qs_d["text"][0]
				text = unquote(text)
				self.embeddings(text)
				return

