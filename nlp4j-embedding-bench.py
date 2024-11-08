import time
import psutil
import torch
from transformers import AutoTokenizer, AutoModel

def measure_embedding_performance(texts, model_name="intfloat/multilingual-e5-large"):
    # トークナイザーとモデルの読み込み
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # GPU が利用可能な場合は GPU を使用
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # メモリ使用量の取得（初期状態）
    process = psutil.Process()
    initial_memory = process.memory_info().rss / (1024 ** 2)  # MB 単位

    # 埋め込みの処理
    start_time = time.time()
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    end_time = time.time()

    # メモリ使用量の取得（処理後）
    final_memory = process.memory_info().rss / (1024 ** 2)  # MB 単位

    # 結果の出力
    print(f"処理時間: {end_time - start_time:.2f} 秒")
    print(f"初期メモリ使用量: {initial_memory:.2f} MB")
    print(f"最終メモリ使用量: {final_memory:.2f} MB")
    print(f"メモリ増加量: {final_memory - initial_memory:.2f} MB")

# サンプルデータ
sample_texts = [
    "This is a sample sentence.",
    "テキストの埋め込み処理を行います。",
    "Voici une phrase d'exemple.",
    "Hier ist ein Beispielsatz.",
    "これはサンプルの文章です。"
]

# パフォーマンス測定
measure_embedding_performance(sample_texts)
