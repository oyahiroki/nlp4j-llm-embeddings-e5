import time
import psutil
import torch
from transformers import AutoTokenizer, AutoModel
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import signal
import sys
import datetime

# モデルとトークナイザーの読み込み
MODEL_NAME = "intfloat/multilingual-e5-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# デバイス設定 (GPU があれば使用)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

signal.signal(signal.SIGINT, signal.SIG_DFL)

class HelloHttpRequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def get_embeddings(self, texts):
        """テキストの埋め込みを取得する"""
        process = psutil.Process()
        initial_memory = process.memory_info().rss / (1024 ** 2)  # 初期メモリ使用量 (MB)

        # 埋め込み処理
        start_time = time.time()
        inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
        with torch.no_grad():
            embeddings = model(**inputs).last_hidden_state.mean(dim=1).cpu().tolist()
        end_time = time.time()

        final_memory = process.memory_info().rss / (1024 ** 2)  # 最終メモリ使用量 (MB)

        # パフォーマンスのログ
        print(f"処理時間: {end_time - start_time:.2f} 秒")
        print(f"メモリ使用量: {final_memory - initial_memory:.2f} MB 増加")

        return embeddings

    def myProcess(self, text):
        try:
            res = {
                "message": "ok",
                "time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "text": text,
                "embeddings": self.get_embeddings([text])[0]
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            print("Error:", e)

    def do_POST(self):
        try:
            content_length = int(self.headers.get('content-length'))
            requestbody = json.loads(self.rfile.read(content_length).decode('utf-8'))
            text = requestbody.get('text')
            self.myProcess(text)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            print("Error:", e)

class HelloHttpServer(ThreadingMixIn, HTTPServer):
    pass

def main():
    ip = '127.0.0.1'
    port = 8888
    server = HelloHttpServer((ip, port), HelloHttpRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
