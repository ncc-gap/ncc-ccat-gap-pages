# ncc-ccat-gap-pages

## How to update

1. markdown ファイル作成

拡張子 `.md` で `markdown/` ディレクトリに作成します。
画像ファイルは `image/` ディレクトリに置きます。

2. HTML ファイルに変換

以下コマンドを実行します。
`markdown/` ディレクトリに存在する拡張子 `.md` のファイルを html に変換して `html/` ディレクトリに出力します。

```Bash
$ python3 ./script/markdown2html.py
```

3. 更新

```Bash
$ git add .
$ git commit -m "message"
$ git push
```
