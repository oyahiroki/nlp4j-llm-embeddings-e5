# 
# Measure embedding performance with a specified input file and model.
# 
# options:
#   -h, --help            show this help message and exit
#   --input_file INPUT_FILE
#                         Path to the input text file.
#   --model_name MODEL_NAME
#                         Model name or path. Default is 'intfloat/multilingual-e5-large'.
import time
import psutil
import torch
from transformers import AutoTokenizer, AutoModel
import argparse
from tqdm import tqdm  # 進行状況バー用

def measure_embedding_performance(input_file=None, model_name="intfloat/multilingual-e5-large"):
    # 入力データの取得
    if input_file:
        with open(input_file, "r", encoding="utf-8") as f:
            texts = f.read().splitlines()  # 改行で区切られたテキストをリストに分割
    else:
        # サンプルデータ
        texts = [
            "This is a sample sentence.",
            "テキストの埋め込み処理を行います。",
            "Voici une phrase d'exemple.",
            "Hier ist ein Beispielsatz.",
            "これはサンプルの文章です。"
        ]

    print(f"処理対象のテキスト件数: {len(texts)} 件")

    # トークナイザーとモデルの読み込み
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # GPU が利用可能な場合は GPU を使用
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # メモリ使用量の取得（初期状態）
    process = psutil.Process()
    initial_memory = process.memory_info().rss / (1024 ** 2)  # MB 単位

    # 1回目のトークナイズと埋め込み処理（初期化のため計測外）
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    with torch.no_grad():
        _ = model(**inputs).last_hidden_state.mean(dim=1)

    # トークナイズの計測
    tokenize_times = []
    print("\nトークナイズ処理中...")
    for text in tqdm(texts, desc="Tokenize Progress"):
        start_time = time.time()
        inputs = tokenizer([text], return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
        end_time = time.time()
        tokenize_times.append(end_time - start_time)

    # 埋め込みの計測
    embedding_times = []
    print("\n埋め込み処理中...")
    for text in tqdm(texts, desc="Embedding Progress"):
        start_time = time.time()
        with torch.no_grad():
            _ = model(**inputs).last_hidden_state.mean(dim=1)
        end_time = time.time()
        embedding_times.append(end_time - start_time)

    # メモリ使用量の取得（処理後）
    final_memory = process.memory_info().rss / (1024 ** 2)  # MB 単位

    # 結果の出力
    print("\n処理結果:")
    print(f"トークナイズの平均時間: {sum(tokenize_times) / len(tokenize_times):.4f} 秒")
    print(f"埋め込み処理の平均時間: {sum(embedding_times) / len(embedding_times):.4f} 秒")
    print(f"初期メモリ使用量: {initial_memory:.2f} MB")
    print(f"最終メモリ使用量: {final_memory:.2f} MB")
    print(f"メモリ増加量: {final_memory - initial_memory:.2f} MB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure embedding performance with a specified input file and model.")
    parser.add_argument("--input_file", type=str, help="Path to the input text file.")
    parser.add_argument("--model_name", type=str, default="intfloat/multilingual-e5-large", help="Model name or path. Default is 'intfloat/multilingual-e5-large'.")

    args = parser.parse_args()
    measure_embedding_performance(input_file=args.input_file, model_name=args.model_name)
