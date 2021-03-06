## 置換 SQL 文ジェネレーター

### 導入手順

1. `replacing-sql-generator` をクローンする
1. Python 3.8 以上をインストールする
1. Poetry のインストール
1. 仮想環境の作成とライブラリのインストール
1. `.csv` ファイルを用意
1. 実行


### Poetry のインストール

```
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

以後、クローンしてきた `replacing-sql-generator` ディレクトリ内で行う


### 仮想環境の作成とライブラリのインストール

完了後、 `.venv` ディレクトリができます

```
poetry config virtualenvs.in-project true
poetry install
```


### API キーのセット

以下コマンドを実行のうえで [PageSpeed Insight API](https://developers.google.com/speed/docs/insights/v5/get-started?hl=ja) より取得した API キーを `.env` の環境変数 `API_KEY` にセットする

```
cp .env .env.example
```


### 実行

`main.py` の変数 `url_list` へ測定する URL をセットする

```
poetry run python main.py
```
