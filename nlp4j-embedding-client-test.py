import requests
import json
import time

# リクエストを送信するURL
url = "http://127.0.0.1:8888/"
params = {"text": "これはテストです。"}

try:
    # リクエスト送信前のタイムスタンプ
    start_time = time.time()
    
    # GETリクエストを送信
    response = requests.get(url, params=params)
    
    # リクエスト送信後のタイムスタンプ
    end_time = time.time()
    
    # レスポンスのステータスコードを確認
    response.raise_for_status()
    
    # JSONレスポンスをパース
    data = response.json()
    
    # 処理時間を計算
    elapsed_time = end_time - start_time
    
    # 結果を表示
    print("Message:", data["message"])
    print("Time:", data["time"])
    print("Text:", data["text"])
    print("Embeddings (first 5):", data["embeddings"][:5])  # 埋め込みの最初の5要素を表示
    print(f"リクエストからレスポンス受信までの時間: {elapsed_time:.4f} 秒")

except requests.exceptions.RequestException as e:
    print(f"HTTPリクエスト中にエラーが発生しました: {e}")
except json.JSONDecodeError as e:
    print(f"JSONのパース中にエラーが発生しました: {e}")

