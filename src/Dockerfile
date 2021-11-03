# ベースイメージを指定する
FROM python:3.9.2
# ポートを公開
EXPOSE 5000

# あとに続く説明の作業ディレクトリを設定
WORKDIR /app

# ファイルとディレクトリをコンテナにコピー
COPY . /app

# コマンド実行でレイヤを作成
# パッケージをコンテナにインストール
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# コマンド実行
CMD [ "python", "app.py" ]