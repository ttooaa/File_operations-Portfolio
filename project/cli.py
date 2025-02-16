import argparse
from project.lib import lib

def main():
    parser = argparse.ArgumentParser(description="ファイル名一括変更ツール")
    parser.add_argument("directory", help="対象ディレクトリのパス")
    parser.add_argument("pattern", help="検索する正規表現パターン")
    parser.add_argument("replacement", help="置換後の文字列")
    parser.add_argument("--preview", action="store_true", help="プレビュー表示のみ（実際の変更は行わない）")
    args = parser.parse_args()

    if args.preview:
        lib.rename_files(args.directory, args.pattern, args.replacement, preview=True)
    else:
        lib.confirm_and_rename(args.directory, args.pattern, args.replacement)

if __name__ == "__main__":
    main()
