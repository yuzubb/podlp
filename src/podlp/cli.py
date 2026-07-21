import argparse
import sys
from .runner import YtDlpPoRunner

def main():
    parser = argparse.ArgumentParser(
        description="YouTube po_token を自動生成して動画をダウンロードするCLIツール"
    )
    parser.add_argument("url", help="ダウンロードしたいYouTube動画のURL")
    parser.add_argument("-f", "--format", help="フォーマット指定", default="best")

    args = parser.parse_args()

    try:
        runner = YtDlpPoRunner()
        extra_opts = {'format': args.format} if args.format else {}
        runner.download(args.url, ytdl_options=extra_opts)
    except KeyboardInterrupt:
        print("\n処理が中断されました。")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
