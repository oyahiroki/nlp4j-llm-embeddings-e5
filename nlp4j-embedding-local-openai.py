import json
import openai
from tqdm import tqdm
import argparse
import time
import os

def embed_text(text, model):
    """OpenAIのembedding APIを使用してテキストを埋め込む関数"""
    try:
        response = openai.Embedding.create(
            model=model,
            input=text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Embedding failed: {e}")
        return None

def process_jsonl(input_file, output_file, text_attr, vector_attr, model):
    """JSONLファイルを読み込み、埋め込み結果を追加して新しいJSONLファイルに書き出す"""
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        total_lines = sum(1 for _ in infile)
        infile.seek(0)  # ファイルポインタを先頭に戻す
        
        for line in tqdm(infile, desc="Processing lines", total=total_lines):
            start_time = time.time()  # 処理開始時間を記録
            data = json.loads(line.strip())
            text = data.get(text_attr)
            if text:
                embedding = embed_text(text, model)
                if embedding:
                    data[vector_attr] = embedding
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
    parser.add_argument("--api-key", help="OpenAI APIキー（環境変数 'OPENAI_API_KEY' が設定されている場合は省略可能）")
    parser.add_argument("--model", default="text-embedding-3-small", help="使用するモデル名（デフォルト: 'text-embedding-3-small')")

    args = parser.parse_args()

    # APIキーの設定
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("APIキーが指定されていません。環境変数 'OPENAI_API_KEY' または '--api-key' で指定してください。")
    openai.api_key = api_key

    # JSONLファイルを処理
    process_jsonl(args.input_file, args.output_file, args.text_attr, args.vector_attr, args.model)

if __name__ == "__main__":
    main()
