import os
import json
import shutil

class OperationHistory:
    def __init__(self, history_file='operation_history.json'):
        self.history_file = history_file
        # 初期化時に履歴をロード
        self.undo_stack = []
        self.redo_stack = []
        self.load_history()

    def load_history(self):
        """履歴ファイルからundo/redoスタックを読み込む"""
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
            # ファイルがなければ空のスタックを用意
            self.undo_stack = []
            self.redo_stack = []

    def save_history(self):
        """現在のundo/redoスタックを履歴ファイルに保存する"""
        data = {
            'undo_stack': self.undo_stack,
            'redo_stack': self.redo_stack,
        }
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("履歴の保存に失敗しました:", e)

    def record(self, old_name, new_name):
        """
        ファイル名変更の操作を記録する。
        操作内容は [old_name, new_name] のリスト形式で保存し、
        Redoスタックはクリアする。
        """
        self.undo_stack.append([old_name, new_name])
        self.redo_stack.clear()
        self.save_history()

    def undo(self, directory):
        """最後の操作を取り消す（Undo）"""
        if not self.undo_stack:
            print("Undo操作はできません。")
            return

        record = self.undo_stack.pop()
        old_name, new_name = record[0], record[1]
        try:
            # 変更後の名前から元の名前に戻す
            shutil.move(os.path.join(directory, new_name), os.path.join(directory, old_name))
            # Undo操作した内容をRedoスタックに追加
            self.redo_stack.append([old_name, new_name])
            self.save_history()
            print(f"Undo: {new_name} -> {old_name}")
        except Exception as e:
            print("Undo操作に失敗しました:", e)

    def redo(self, directory):
        """最後に取り消した操作を再実行する（Redo）"""
        if not self.redo_stack:
            print("Redo操作はできません。")
            return

        record = self.redo_stack.pop()
        old_name, new_name = record[0], record[1]
        try:
            # 元の名前から再度新しい名前に変更
            shutil.move(os.path.join(directory, old_name), os.path.join(directory, new_name))
            self.undo_stack.append([old_name, new_name])
            self.save_history()
            print(f"Redo: {old_name} -> {new_name}")
        except Exception as e:
            print("Redo操作に失敗しました:", e)
