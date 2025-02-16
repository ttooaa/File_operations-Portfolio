import os
import json
import shutil

class OperationHistory:
    def __init__(self, history_file='operation_history.json'):
        # 履歴ファイル名（相対パス）。実行時のカレントディレクトリに作成される
        self.history_file = history_file
        # UndoおよびRedo操作用のスタックを初期化
        self.undo_stack = []
        self.redo_stack = []
        # 履歴ファイルから既存の操作履歴を読み込む
        self.load_history()

    def load_history(self):
        """
        履歴ファイルからundo/redoのスタックを読み込み、内部変数にセットする
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.undo_stack = data.get('undo_stack', [])
                    self.redo_stack = data.get('redo_stack', [])
            except Exception as e:
                print("履歴の読み込みに失敗しました:", e)
                self.undo_stack = []
                self.redo_stack = []
        else:
            # 履歴ファイルが存在しない場合は、空のスタックを初期化
            self.undo_stack = []
            self.redo_stack = []

    def save_history(self):
        """
        現在のundo/redoスタックを履歴ファイルに保存する
        """
        data = {
            'undo_stack': self.undo_stack,
            'redo_stack': self.redo_stack,
        }
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("履歴の保存に失敗しました:", e)

    def record_operation(self, op):
        """
        操作（op）をundoスタックに追加し、redoスタックをクリアした上で、
        履歴ファイルに保存する。
        """
        self.undo_stack.append(op)
        self.redo_stack.clear()
        self.save_history()

    def record_rename(self, old_name, new_name):
        """
        ファイル名変更操作を記録する
        """
        op = {"type": "rename", "old": old_name, "new": new_name}
        self.record_operation(op)

    def record_create(self, folder_list):
        """
        フォルダ作成操作を記録する
        """
        op = {"type": "create", "folders": folder_list}
        self.record_operation(op)

    def record_delete(self, folder_list):
        """
        フォルダ削除操作を記録する
        """
        op = {"type": "delete", "folders": folder_list}
        self.record_operation(op)

    def undo(self, directory):
        """
        最後に記録された操作を取り消す（Undo）。
        操作の種類に応じて、ファイル名変更、フォルダ作成、フォルダ削除の各Undo処理を実行する。
        """
        if not self.undo_stack:
            print("Undo操作はできません。")
            return

        op = self.undo_stack.pop()
        if op["type"] == "rename":
            # ファイル名変更のUndo処理：変更後の名前から元の名前に戻す
            old_name = op["old"]
            new_name = op["new"]
            try:
                shutil.move(os.path.join(directory, new_name), os.path.join(directory, old_name))
                print(f"Undo rename: {new_name} -> {old_name}")
            except Exception as e:
                print("Undo操作（rename）に失敗しました:", e)
                return
        elif op["type"] == "create":
            # フォルダ作成のUndo処理：作成されたフォルダを削除する
            for folder in op["folders"]:
                folder_path = os.path.join(directory, folder)
                try:
                    os.rmdir(folder_path)
                    print(f"Undo create: Removed folder {folder}")
                except Exception as e:
                    print(f"Undo create: Failed to remove folder {folder}: {e}")
        elif op["type"] == "delete":
            # フォルダ削除のUndo処理：削除されたフォルダを再作成する
            for folder in op["folders"]:
                folder_path = os.path.join(directory, folder)
                try:
                    os.mkdir(folder_path)
                    print(f"Undo delete: Created folder {folder}")
                except Exception as e:
                    print(f"Undo delete: Failed to create folder {folder}: {e}")
        else:
            print("不明な操作タイプ:", op.get("type"))
            return

        # Undoした操作をredoスタックに追加する
        self.redo_stack.append(op)
        self.save_history()

    def redo(self, directory):
        """
        Undoで取り消した操作を再度実行する（Redo）。
        操作の種類に応じて、ファイル名変更、フォルダ作成、フォルダ削除の各Redo処理を実施する。
        """
        if not self.redo_stack:
            print("Redo操作はできません。")
            return

        op = self.redo_stack.pop()
        if op["type"] == "rename":
            # ファイル名変更のRedo処理：元の名前から再度新しい名前に変更する
            old_name = op["old"]
            new_name = op["new"]
            try:
                shutil.move(os.path.join(directory, old_name), os.path.join(directory, new_name))
                print(f"Redo rename: {old_name} -> {new_name}")
            except Exception as e:
                print("Redo操作（rename）に失敗しました:", e)
                return
        elif op["type"] == "create":
            # フォルダ作成のRedo処理：再度フォルダを作成する
            for folder in op["folders"]:
                folder_path = os.path.join(directory, folder)
                try:
                    os.mkdir(folder_path)
                    print(f"Redo create: Created folder {folder}")
                except Exception as e:
                    print(f"Redo create: Failed to create folder {folder}: {e}")
        elif op["type"] == "delete":
            # フォルダ削除のRedo処理：再度フォルダを削除する
            for folder in op["folders"]:
                folder_path = os.path.join(directory, folder)
                try:
                    os.rmdir(folder_path)
                    print(f"Redo delete: Removed folder {folder}")
                except Exception as e:
                    print(f"Redo delete: Failed to remove folder {folder}: {e}")
        else:
            print("不明な操作タイプ:", op.get("type"))
            return

        # Redoした操作をundoスタックに追加する
        self.undo_stack.append(op)
        self.save_history()
