このプロジェクトは、Python を用いてファイルやフォルダの操作を一括で行うためのツールです。  
本機能はコマンドラインからのみ実行可能です。

## 機能一覧

- **ファイル名の一括変更 (rename)**
  - 指定ディレクトリ内のファイル名に対して、正規表現を用いた一括変更を実行します。
  - プレビュー表示機能により、実際の変更前に内容を確認可能です。

- **フォルダ作成 (create)**
  - 指定ディレクトリ内に、指定した数だけ10区切りの名前（例："10_", "20_", …）のフォルダを作成します。
  - 作成前のプレビュー表示およびユーザー確認を行います。

- **フォルダ削除 (delete)**
  - 指定ディレクトリ内に存在するすべてのサブフォルダを削除します。
  - 削除対象のフォルダが一つも存在しない場合は、その旨の内容を表示します。
  - 削除前にプレビュー表示し、ユーザー確認を実施します。

- **Undo/Redo 機能**
  - 各操作（ファイル名変更、フォルダ作成、フォルダ削除）の履歴を JSON 形式で保存し、プロセス間で保持します。
  - Undo コマンドで直前の操作を取り消し、Redo コマンドで取り消し操作を再実行できます。

## ファイル構成
File_operations-Portfolio(root) /
 ├─ project / 
 │   ├─ __init__.py
 │   ├─ __main__.py    # エントリーポイント（cli.pyを呼び出す）
 │   ├─ cli.py         # コマンドライン引数の解釈と各機能への振り分け
 │   ├─ lib / 
 │      ├─ __init__.py
 │      ├─ lib.py      # ファイル・フォルダ操作（rename, create, delete）の実装
 │      ├─ history.py  # 操作履歴の管理とUndo/Redo機能の実装


## 操作方法
※コマンドライン上で操作を行います。
### 1. rename コマンド
#### ＜使用例＞

python -m project rename "C:\path\to\directory" "^old" "new"

#### ＜実行結果例＞

【プレビュー】
old_file.txt -> new_file.txt
old_image.jpg -> new_image.jpg
上記の内容でファイル名を変更してよろしいですか？ (y/n): y
変更: old_file.txt -> new_file.txt
変更: old_image.jpg -> new_image.jpg
ファイル名の変更が完了しました。
### 2. create コマンド
#### ＜使用例＞

python -m project create "C:\path\to\directory" 3

#### ＜実行結果例＞

【プレビュー】
10_
20_
30_
上記の内容でフォルダを作成してよろしいですか？ (y/n): y
Created folder: 10_
Created folder: 20_
Created folder: 30_
フォルダ作成が完了しました。

### 3. delete コマンド
#### ＜使用例＞

python -m project delete "C:\path\to\directory"

#### ＜実行結果例＞

【プレビュー】
10_
20_
30_
その他のサブフォルダも含む全フォルダが一覧表示されます。
上記の内容でフォルダを削除してよろしいですか？ (y/n): y
Deleted folder: 10_
Deleted folder: 20_
Deleted folder: 30_
（その他、削除対象のフォルダが削除される）
フォルダの削除が完了しました。
