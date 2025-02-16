import argparse
from project.lib import lib

def main():
    # コマンドライン引数の解析のためのパーサーを作成
    parser = argparse.ArgumentParser(description="ファイル名一括変更ツール")
    # サブコマンドを利用して、実行する機能を選択する
    subparsers = parser.add_subparsers(dest="command", help="実行するコマンドを選択")

    # 【rename】コマンド → ファイル名を変更する
    rename_parser = subparsers.add_parser("rename", help="ファイル名を変更する")
    rename_parser.add_argument("directory", help="対象ディレクトリのパス")
    rename_parser.add_argument("pattern", help="検索する正規表現パターン")
    rename_parser.add_argument("replacement", help="置換後の文字列")
    rename_parser.add_argument("--preview", action="store_true", help="プレビュー表示のみ")

    # 【create】コマンド → 指定数のフォルダを作成する
    create_parser = subparsers.add_parser("create", help="指定数のフォルダを作成する")
    create_parser.add_argument("directory", help="対象ディレクトリのパス")
    create_parser.add_argument("count", type=int, help="作成するフォルダの数")
    create_parser.add_argument("--preview", action="store_true", help="プレビュー表示のみ")

    # 【delete】コマンド → 指定ディレクトリ内のすべてのフォルダを削除する
    delete_parser = subparsers.add_parser("delete", help="指定ディレクトリ内のすべてのフォルダを削除する")
    delete_parser.add_argument("directory", help="対象ディレクトリのパス")
    delete_parser.add_argument("--preview", action="store_true", help="プレビュー表示のみ")

    # 【undo】コマンド → 最後に行った操作を取り消す（Undo）
    undo_parser = subparsers.add_parser("undo", help="最後の操作を取り消す")
    undo_parser.add_argument("directory", help="対象ディレクトリのパス")

    # 【redo】コマンド → Undoした操作を再実行する（Redo）
    redo_parser = subparsers.add_parser("redo", help="最後に取り消した操作を再実行する")
    redo_parser.add_argument("directory", help="対象ディレクトリのパス")

    # コマンドライン引数の解析結果を取得
    args = parser.parse_args()

    # 指定されたサブコマンドに応じて処理を振り分ける
    if args.command == "rename":
        if args.preview:
            lib.rename_files(args.directory, args.pattern, args.replacement, preview=True)
        else:
            lib.rename_files(args.directory, args.pattern, args.replacement)
    elif args.command == "create":
        if args.preview:
            lib.create_folders(args.directory, args.count, preview=True)
        else:
            lib.create_folders(args.directory, args.count)
    elif args.command == "delete":
        if args.preview:
            lib.delete_all_folders(args.directory, preview=True)
        else:
            lib.delete_all_folders(args.directory)
    elif args.command == "undo":
        lib.history.undo(args.directory)
    elif args.command == "redo":
        lib.history.redo(args.directory)
    else:
        # サブコマンドが指定されなかった場合はヘルプを表示
        parser.print_help()

if __name__ == "__main__":
    main()