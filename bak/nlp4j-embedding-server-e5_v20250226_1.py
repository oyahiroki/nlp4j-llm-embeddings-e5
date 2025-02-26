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

signal.signal(signal.SIGINT, signal.SIG_DFL)

def sig_handler(signum, frame) -> None:
    sys.exit(1)

print("initializing ... 1/2")
model = SentenceTransformer('intfloat/multilingual-e5-large')  # モデルの一度きりの初期化
print("initializing ... 2/2")
model.encode(["test"])
print("initializing ... done")



class HelloHttpRequestHandler(BaseHTTPRequestHandler):
    count = 0

    def log_message(self, format, *args):
        pass
    
    def embeddings(self, text):
        HelloHttpRequestHandler.count += 1
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
        HelloHttpRequestHandler.count += 1
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
	        self.semanticsearch(text1,text2)
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
	        if "text" not in qs_d:
	            self.send_response(404)
	            self.end_headers()
	            return
	        text = qs_d["text"][0]
	        text = unquote(text)
	        self.embeddings(text)
	        return

class HelloHttpServer(ThreadingMixIn, HTTPServer):
    pass


def main():
    signal.signal(signal.SIGTERM, sig_handler)
#    ip = '127.0.0.1'
    ip = '0.0.0.0'
    
    parser = argparse.ArgumentParser(description="nlp4j-embedding")
    parser.add_argument("-p", "--port", type=int, default=8888, help="Port Number")
    args = parser.parse_args()	
    
    port = args.port
	
    print("http://" + ip + ":" + str(port) + "/embeddings?text=これはテストです。")
    print("http://" + ip + ":" + str(port) + "/embeddings?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82")
    print("curl -X POST -H \"Content-Type: application/json\" -d \"{\\\"text\\\":\\\"これはテストです。\\\"}\" http://" + ip + ":" + str(port) + "/embeddings")
    print("Expected response: " + '{"message": "ok", "time": "2024-05-26T23:21:38", "text": "\u3053\u308c\u306f\u30c6\u30b9\u30c8\u3067\u3059\u3002", "embeddings": [0.04231283441185951, -0.0035561583936214447, -0.014567600563168526, ... 0.022928446531295776]}')
    print()
    print("http://" + ip + ":" + str(port) + "/semanticsearch?text1=これはテストです。&text2=これは試験です。")
    print("curl -X POST -H \"Content-Type: application/json\" -d \"{\\\"text1\\\":\\\"これはテストです。\\\",\\\"text2\\\":\\\"これは試験です。\\\"}\" http://" + ip + ":" + str(port) + "/embeddings")
    
    # これはテストです
    # これは試験です
    # http://localhost:8888/semanticsearch?text1=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99&text2=%E3%81%93%E3%82%8C%E3%81%AF%E8%A9%A6%E9%A8%93%E3%81%A7%E3%81%99
    
    server = HelloHttpServer((ip, port), HelloHttpRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
