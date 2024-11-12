# coding: utf-8

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import json
import traceback
from socketserver import ThreadingMixIn
import sys
import time
import datetime
import signal
from sentence_transformers import SentenceTransformer

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
    
    def myProcess(self, text):
        HelloHttpRequestHandler.count += 1
        try:
            time1 = time.time()
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

            time2 = time.time()
            
            # 処理時間の出力
            print("Embedding Time: {:.6f} seconds".format(embed_end_time - embed_start_time))
            
            del html, res, time2, time1
        except Exception as e:
            print(traceback.format_exc())
            self.send_response(500)
    
    def do_POST(self):
        content_length = int(self.headers.get('content-length'))
        request_body = json.loads(self.rfile.read(content_length).decode('utf-8'))
        text = request_body.get('text')
        self.myProcess(text)
    
    def do_GET(self):
        query = urlparse(self.path).query
        qs_d = parse_qs(query)
        if "text" not in qs_d:
            self.send_response(404)
            self.end_headers()
            return
        text = qs_d["text"][0]
        text = unquote(text)
        self.myProcess(text)

class HelloHttpServer(ThreadingMixIn, HTTPServer):
    pass


def main():
    signal.signal(signal.SIGTERM, sig_handler)
    ip = '127.0.0.1'
    port = 8888
    args = sys.argv[1:]
    if len(args) == 1:
        port = int(args[0])
    print("http://" + ip + ":" + str(port) + "/?text=これはテストです。")
    print("http://" + ip + ":" + str(port) + "/?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82")
    print("curl -X POST -H \"Content-Type: application/json\" -d \"{\\\"text\\\":\\\"これはテストです。\\\"}\" http://" + ip + ":" + str(port) + "/")
    print("Expected response: " + '{"message": "ok", "time": "2024-05-26T23:21:38", "text": "\u3053\u308c\u306f\u30c6\u30b9\u30c8\u3067\u3059\u3002", "embeddings": [0.04231283441185951, -0.0035561583936214447, -0.014567600563168526, ... 0.022928446531295776]}')
    server = HelloHttpServer((ip, port), HelloHttpRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
