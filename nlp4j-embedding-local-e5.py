import json
import torch
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
import argparse
import time

# モデルとトークナイザーの初期化
model_name = "intfloat/multilingual-e5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# GPU が利用可能な場合は GPU を使用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def embed_text(text):
    """テキストを埋め込む関数"""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.cpu().tolist()[0]

def process_jsonl(input_file, output_file, text_attr, vector_attr):
    """JSONLファイルを読み込み、埋め込み結果を追加して新しいJSONLファイルに書き出す"""
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        total_lines = sum(1 for _ in infile)
        infile.seek(0)  # ファイルポインタを先頭に戻す
        
        for line in tqdm(infile, desc="Processing lines", total=total_lines):
            start_time = time.time()  # 処理開始時間を記録
            data = json.loads(line.strip())
            text = data.get(text_attr)
            if text:
                data[vector_attr] = embed_text(text)
            end_time = time.time()  # 処理終了時間を記録
            elapsed_time = end_time - start_time  # 処理時間を計算
            print(f"1件あたりの処理時間: {elapsed_time:.4f} 秒")
            
            json.dump(data, outfile, ensure_ascii=False)
            outfile.write('\n')

def main():
    # コマンドライン引数のパーサーを設定
    parser = argparse.ArgumentParser(description="JSONLファイルを読み込み、指定された属性を埋め込み、結果を新しいJSONLに書き出します。")
    parser.add_argument("input_file", help="入力JSONLファイルのパス")
    parser.add_argument("output_file", help="出力JSONLファイルのパス")
    parser.add_argument("--text-attr", default="text", help="テキストを取得する属性名（デフォルト: 'text')")
    parser.add_argument("--vector-attr", default="vector", help="ベクトルをセットする属性名（デフォルト: 'vector')")
    
    args = parser.parse_args()

    # JSONLファイルを処理
    process_jsonl(args.input_file, args.output_file, args.text_attr, args.vector_attr)

if __name__ == "__main__":
    main()
