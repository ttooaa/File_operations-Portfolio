import os
import re
import shutil
from project.lib.history import OperationHistory

# グローバルな履歴管理インスタンスを作成
history = OperationHistory()

def rename_files(directory, pattern, replacement, preview=False):
    """
    指定ディレクトリ内で、patternにマッチするファイル名を
    replacementに沿って変更する（プレビューのみの場合は変更しない）。
    """
    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        print("指定されたディレクトリが見つかりません。")
        return

    # 正規表現でマッチするファイルを抽出
    matched_files = [f for f in files if re.search(pattern, f)]
    if not matched_files:
        print("該当するファイルが見つかりません。")
        return

    print("【プレビュー】")
    for old_name in matched_files:
        new_name = re.sub(pattern, replacement, old_name)
        print(f"{old_name} -> {new_name}")

    if preview:
        return

    # ユーザーに確認
    confirm = input("上記の内容でファイル名を変更してよろしいですか？ (y/n): ")
    if confirm.lower() != 'y':
        print("操作をキャンセルしました。")
        return

    # 実際にファイル名を変更
    for old_name in matched_files:
        new_name = re.sub(pattern, replacement, old_name)
        src = os.path.join(directory, old_name)
        dst = os.path.join(directory, new_name)
        try:
            shutil.move(src, dst)
            print(f"変更: {old_name} -> {new_name}")
            # 操作履歴を記録する
            history.record(old_name, new_name)
        except Exception as e:
            print(f"エラー: {old_name} の変更に失敗しました。詳細: {e}")
    print("ファイル名の変更が完了しました。")


def confirm_and_rename(directory, pattern, replacement):
    """
    ユーザー確認後にファイル名を変更するラッパー関数。
    """
    rename_files(directory, pattern, replacement, preview=False)
