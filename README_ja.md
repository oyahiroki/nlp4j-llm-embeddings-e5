# Multilingual E5 Embedding Server

https://github.com/oyahiroki/nlp4j-llm-embeddings-e5

## 概要

**nlp4j-llm-embeddings-e5**は、E5モデルを使用した多言語対応の埋め込みベクトル生成サーバーです。sentence-transformersをベースに構築され、テキスト処理タスクのための使いやすいREST APIインターフェースを提供します。

## 主な機能

### 1. Embeddings API (`/embeddings`)
テキストをベクトル埋め込みに変換します。文書検索用にE5の"passage:"プレフィックスが自動的に付与されます。

### 2. Semantic Search API (`/semantic_search`)
クエリとコーパス間のセマンティック検索を実行します。クエリには"query:"、コーパスには"passage:"プレフィックスが自動付与されます。

### 3. Cosine Similarity API (`/cos_sim`)
2つのテキスト間のコサイン類似度を計算します。

## 前提条件

Python 3.10以上が必要です。

```bash
$ python3 --version
Python 3.10.12
```

## インストール

以下の手順でセットアップを行います：

### 1. リポジトリのクローン

```bash
git clone https://github.com/oyahiroki/nlp4j-llm-embeddings-e5.git
```

### 2. プロジェクトディレクトリへ移動

```bash
cd nlp4j-llm-embeddings-e5
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

## サーバーの起動

以下のコマンドでサーバーを起動します：

```bash
python3 nlp4j-embedding-server-e5.py
```

### オプション引数

- `--host`: バインドするホスト（デフォルト: 127.0.0.1）
- `-p, --port`: ポート番号（デフォルト: 8888）

例：
```bash
python3 nlp4j-embedding-server-e5.py --host 0.0.0.0 --port 9000
```

## API使用方法

サーバーはテキストを送信し、その埋め込みベクトルを受信するためのREST APIを提供します。以下はGETおよびPOSTリクエストの使用例です。

### Embeddings API

#### GETリクエスト（プレーンテキスト）

エンコードなしでプレーンテキストクエリを送信：

```bash
curl http://127.0.0.1:8888/embeddings?text=これはテストです。
```

#### GETリクエスト（URLエンコード）

URLエンコードされたテキストクエリを送信：

```bash
curl http://127.0.0.1:8888/embeddings?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82
```

#### POSTリクエスト（JSONボディ）

JSONリクエストボディでテキストを送信：

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"これはテストです。"}' \
  http://127.0.0.1:8888/embeddings
```

#### トークン数チェック付きリクエスト

```bash
curl http://127.0.0.1:8888/embeddings?text=これはテストです。&checktokencount=true
```

#### レスポンス例

```json
{
  "message": "ok",
  "time": "2024-05-26T23:21:38",
  "text": "これはテストです。",
  "embeddings": [0.04231283441185951, -0.0035561583936214447, -0.014567600563168526, ...]
}
```

トークン数チェック付きの場合：
```json
{
  "message": "ok",
  "time": "2024-05-26T23:21:38",
  "text": "これはテストです。",
  "token_count": 15,
  "max_tokens": 512,
  "truncated": false,
  "embeddings": [...]
}
```

### Semantic Search API

#### GETリクエスト

```bash
curl "http://127.0.0.1:8888/semantic_search?text1=これはテストです。&text2=これは試験です。"
```

#### POSTリクエスト（複数文書）

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"これはテストです。","texts":["これは試験です。","これは検査です。"]}' \
  http://127.0.0.1:8888/semantic_search
```

#### レスポンス例

```json
{
  "message": "ok",
  "time": "2024-05-26T23:21:38",
  "text": "これはテストです。",
  "r": [
    {"corpus_id": 0, "score": 0.8234},
    {"corpus_id": 1, "score": 0.7891}
  ]
}
```

### Cosine Similarity API

#### GETリクエスト

```bash
curl "http://127.0.0.1:8888/cos_sim?text1=これはテストです。&text2=これは試験です。"
```

#### POSTリクエスト

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text1":"これはテストです。","text2":"これは試験です。"}' \
  http://127.0.0.1:8888/cos_sim
```

#### トークン数チェック付きリクエスト

```bash
curl "http://127.0.0.1:8888/cos_sim?text1=これはテストです。&text2=これは試験です。&checktokencount=true"
```

#### レスポンス例

```json
{
  "text1": "これはテストです。",
  "text2": "これは試験です。",
  "cosine_similarity": 0.8234567
}
```

トークン数チェック付きの場合：
```json
{
  "text1": "これはテストです。",
  "text2": "これは試験です。",
  "max_tokens": 512,
  "token_count1": 15,
  "token_count2": 14,
  "truncated1": false,
  "truncated2": false,
  "cosine_similarity": 0.8234567
}
```

## REST API概要

このAPIは、HTTPリクエストを通じて様々なアプリケーションへの簡単な統合を可能にします。サーバーはGETとPOSTの両方のメソッドをサポートしています。

- **GET**: クエリパラメータとしてテキストを渡すシンプルで高速な方法
- **POST**: 構造化データに最適で、複雑なリクエストのためのJSONペイロードが可能

## REST API統合の利点

- **言語非依存**: HTTPリクエストを送信できる任意のプログラミング言語（Python、Java、JavaScript、Rubyなど）で使用可能
- **統合の容易さ**: サーバー側のコードを変更する必要がなく、APIはすぐに使用可能
- **スケーラビリティ**: 複数の同時リクエストを処理でき、本番環境のワークロードに適している

## Docker対応

### Dockerイメージのビルド

```bash
docker build -t nlp4j-llm-embeddings-e5 ./docker
```

または、特定のバージョンタグ付きで：

```bash
docker build --no-cache -t oyahiroki/nlp4j-llm-embeddings-e5:1.0.0.0 ./docker
```

### コンテナの実行

```bash
docker run -d --name nlp4j-llm-embeddings-e5 -p 8888:8888 nlp4j-llm-embeddings-e5
```

### テスト

```bash
curl http://127.0.0.1:8888/embeddings?text=%E3%81%93%E3%82%8C%E3%81%AF%E3%83%86%E3%82%B9%E3%83%88%E3%81%A7%E3%81%99%E3%80%82
```

詳細は[docker/README.md](docker/README.md)を参照してください。

## Multilingual E5 Embeddingについて

Hugging Faceで利用可能なMultilingual E5 Embeddingは、94言語での特徴抽出用に設計された大規模言語モデルです。

### 基盤とトレーニングデータ

XLM-RoBERTaをベースとし、多様な多言語データセットでトレーニングされており、テキスト検索やセマンティック類似度などの様々なタスクのためのテキストエンコーディング能力を強化しています。

### パフォーマンスと応用

このモデルは、特に多言語環境において、様々なベンチマークで高いパフォーマンスを達成しています。

### 実装と統合

PyTorchで実装され、Sentence Transformersと互換性があり、アプリケーションへの統合が容易です。

詳細については、[Hugging Faceページ](https://huggingface.co/intfloat/multilingual-e5-large)をご覧ください。

## パフォーマンス例

### リソース使用量

```bash
$ ps aux | grep python
oyahiro+   832  0.0  4.1 128670360 4127176 pts/3 Sl Jul17   0:32 python3 nlp4j-embedding-server-e5.py
```

### GPU使用状況（NVIDIA GeForce RTX 3060 Ti）

```bash
$ nvidia-smi
Thu Jul 18 01:03:18 2024
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.54.10              Driver Version: 551.61         CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 3060 Ti     On  |   00000000:01:00.0 Off |                  N/A |
| 30%   32C    P8             10W /  200W |    3737MiB /   8192MiB |     12%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
```

### 処理時間

NVIDIA GeForce RTX 3060 Ti使用時、埋め込み生成にかかる時間は0.05〜0.1秒です。

```bash
$ curl -w"time_total: %{time_total}\n" -X POST -H "Content-Type: application/json" \
  -d '{"text":"これはテストです。"}' http://127.0.0.1:8888/embeddings

{"message": "ok", "time": "2024-07-19T16:25:52", "text": "これはテストです。", 
 "embeddings": [0.04231283441185951, -0.0035561583936214447, ...]}
time_total: 0.058588
```

## テストスクリプト

プロジェクトには、APIをテストするためのサンプルスクリプトが含まれています：

### Embeddingsテスト

```bash
python3 bin/nlp4j-embedding-server-e5-test-embedding.py
```

### Cosine Similarityテスト

```bash
python3 bin/nlp4j-embedding-server-e5-test-cos_sim.py
```

## ユーティリティツール

### ローカル埋め込み処理

JSONLファイルをバッチ処理するためのツール：

```bash
python3 bin/nlp4j-embedding-local-e5.py input.jsonl output.jsonl --text-attr text --vector-attr vector
```

## プロジェクト構造

```
nlp4j-llm-embeddings-e5/
├── nlp4j-embedding-server-e5.py          # メインサーバー
├── requirements.txt                       # 依存パッケージ
├── README.md                              # 英語版README
├── README_ja.md                           # 日本語版README（このファイル）
├── LICENSE.txt                            # Apache License 2.0
├── bin/                                   # ユーティリティとテストスクリプト
│   ├── nlp4j_embedding_server_requesthandler.py  # リクエストハンドラ
│   ├── nlp4j-embedding-server-e5-test-embedding.py
│   ├── nlp4j-embedding-server-e5-test-cos_sim.py
│   ├── nlp4j-embedding-local-e5.py
│   └── nlp4j-embedding-local-openai.py
├── docker/                                # Docker設定
│   ├── Dockerfile
│   └── README.md
├── html/                                  # Webインターフェース
│   └── index.html
└── bak/                                   # バックアップファイル
```

## 技術仕様

- **モデル**: intfloat/multilingual-e5-large
- **ベースモデル**: XLM-RoBERTa
- **対応言語**: 94言語
- **最大トークン数**: 512
- **埋め込み次元**: 1024
- **正規化**: L2正規化済み

## E5プレフィックスについて

E5モデルは、最適なパフォーマンスのために特定のプレフィックスを使用します：

- **passage:**: 文書やコーパスの埋め込み用（検索対象）
- **query:**: クエリの埋め込み用（検索元）

このサーバーは、適切なエンドポイントで自動的にこれらのプレフィックスを付与します。

## トラブルシューティング

### モデルのダウンロードに時間がかかる

初回起動時、モデルが自動的にダウンロードされます（約2GB）。これは一度だけ実行されます。

### メモリ不足エラー

- GPU使用時: 最低8GB VRAMを推奨
- CPU使用時: 最低8GB RAMを推奨

### ポートが既に使用されている

別のポートを指定してください：
```bash
python3 nlp4j-embedding-server-e5.py --port 9000
```

## ライセンス

Apache License 2.0

Copyright 2024 Hiroki Oya (NLP4J)

詳細は[LICENSE.txt](LICENSE.txt)を参照してください。

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。

## サポート

問題や質問がある場合は、GitHubのissueを作成してください：
https://github.com/oyahiroki/nlp4j-llm-embeddings-e5/issues

## まとめ

このプロジェクトは、多言語テキスト埋め込みを生成するための高効率なソリューションを提供します。REST APIは柔軟性を提供し、検索、レコメンデーション、セマンティック分析などの自然言語処理タスクにとって価値あるツールとなっています。