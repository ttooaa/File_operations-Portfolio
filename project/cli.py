import argparse
from project.lib import lib

def main():
    parser = argparse.ArgumentParser(description="ファイル名一括変更ツール")
    parser.add_argument("directory", help="対象ディレクトリのパス")
    parser.add_argument("pattern", help="検索する正規表現パターン")
    parser.add_argument("replacement", help="置換後の文字列")
    parser.add_argument("--preview", action="store_true", help="プレビュー表示のみ（実際の変更は行わない）")
    parser.add_argument("--undo", action="store_true", help="最後の操作を取り消す")
    parser.add_argument("--redo", action="store_true", help="最後に取り消した操作を再実行する")
    args = parser.parse_args()

    if args.undo:
        # Undo 操作（ディレクトリは必ず指定）
        if args.directory:
            lib.history.undo(args.directory)
        else:
            print("Undoを実行するにはディレクトリの指定が必要です。")
    elif args.redo:
        # Redo 操作（ディレクトリは必ず指定）
        if args.directory:
            lib.history.redo(args.directory)
        else:
            print("Redoを実行するにはディレクトリの指定が必要です。")
    elif args.directory and args.pattern and args.replacement:
        if args.preview:
            lib.rename_files(args.directory, args.pattern, args.replacement, preview=True)
        else:
            lib.rename_files(args.directory, args.pattern, args.replacement)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
