import os
import re
import shutil
from project.lib.history import OperationHistory

# グローバルな履歴管理インスタンスを作成
history = OperationHistory()

def rename_files(directory, pattern, replacement, preview=False):
    """
    指定されたディレクトリ内で、ファイル名に対して正規表現のパターンを適用し、
    マッチした部分を置換文字列に変更する処理を行う。

    ・preview=Trueの場合、実際には変更せずにプレビューのみ表示する。
    ・変更後、成功した操作は履歴に記録される（Undo/Redo対応）。
    """
    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        print("指定されたディレクトリが見つかりません。")
        return

    # 指定されたパターンにマッチするファイルのみを抽出
    matched_files = [f for f in files if re.search(pattern, f)]
    if not matched_files:
        print("該当するファイルが見つかりません。")
        return

    # プレビュー表示：変更前後のファイル名を出力
    print("【プレビュー】")
    for old_name in matched_files:
        new_name = re.sub(pattern, replacement, old_name)
        print(f"{old_name} -> {new_name}")

    if preview:
        return

    # ユーザーに変更内容の確認を促す
    confirm = input("上記の内容でファイル名を変更してよろしいですか？ (y/n): ")
    if confirm.lower() != 'y':
        print("操作をキャンセルしました。")
        return

    # 実際にファイル名を変更し、操作履歴に記録する
    for old_name in matched_files:
        new_name = re.sub(pattern, replacement, old_name)
        src = os.path.join(directory, old_name)
        dst = os.path.join(directory, new_name)
        try:
            shutil.move(src, dst)
            print(f"変更: {old_name} -> {new_name}")
            # リネーム操作を履歴に記録
            history.record_rename(old_name, new_name)
        except Exception as e:
            print(f"エラー: {old_name} の変更に失敗しました。詳細: {e}")
    print("ファイル名の変更が完了しました。")

def create_folders(directory, count, preview=False):
    """
    指定されたディレクトリ内に、指定数(count)のフォルダを作成する。

    ・フォルダ名は 10区切りとなり、例えば count=1 の場合は "10_"、count=2 の場合は "10_" と "20_" を作成する。
    ・preview=Trueの場合、実際には作成せずプレビューのみ表示する。
    ・作成したフォルダは履歴に記録される（Undo/Redo対応）。
    """

    # count に応じたフォルダ名リストを生成（10,20,30,...）
    folder_names = [f"{i*10}_" for i in range(1, count+1)]
    print("【プレビュー】")
    for name in folder_names:
        print(name)

    if preview:
        return

    # ユーザーに作成内容を確認させる
    confirm = input("上記の内容でフォルダを作成してよろしいですか？ (y/n): ")
    if confirm.lower() != 'y':
        print("操作をキャンセルしました。")
        return

    created_folders = []
    # 各フォルダを作成する
    for folder in folder_names:
        folder_path = os.path.join(directory, folder)
        try:
            os.mkdir(folder_path)
            print(f"Created folder: {folder}")
            created_folders.append(folder)
        except Exception as e:
            print(f"Failed to create folder {folder}: {e}")

    # 作成に成功したフォルダがあれば履歴に記録する
    if created_folders:
        history.record_create(created_folders)
    print("フォルダ作成が完了しました。")

def delete_all_folders(directory, preview=False):
    """
    指定されたディレクトリ内にある全てのサブフォルダを削除する。

    ・削除対象のフォルダが一つも存在しない場合は、その旨を表示する。
    ・preview=Trueの場合、実際の削除は行わずプレビューのみ表示する。
    ・削除したフォルダは履歴に記録される（Undo/Redo対応）。
    """
    try:
        items = os.listdir(directory)
    except FileNotFoundError:
        print("指定されたディレクトリが見つかりません。")
        return

    # ディレクトリ内のサブフォルダのみを抽出
    folder_names = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    if not folder_names:
        print("削除するフォルダは存在しません。")
        return

    # プレビュー表示
    print("【プレビュー】")
    for folder in folder_names:
        print(folder)

    if preview:
        return

    # ユーザーに削除内容の確認を促す
    confirm = input("上記の内容でフォルダを削除してよろしいですか？ (y/n): ")
    if confirm.lower() != 'y':
        print("操作をキャンセルしました。")
        return

    deleted_folders = []
    # 各サブフォルダを削除する（※空のフォルダのみ削除可能）
    for folder in folder_names:
        folder_path = os.path.join(directory, folder)
        try:
            os.rmdir(folder_path)
            print(f"Deleted folder: {folder}")
            deleted_folders.append(folder)
        except Exception as e:
            print(f"Failed to delete folder {folder}: {e}")

    # 削除したフォルダがあれば履歴に記録する
    if deleted_folders:
        history.record_delete(deleted_folders)
    print("フォルダの削除が完了しました。")