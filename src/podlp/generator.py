import os
import sys
import subprocess
import json
from typing import Dict

class NativePoTokenGenerator:
    """JSランナーを実行して po_token を生成するクラス"""

    def __init__(self, js_runner_path: str = None):
        if js_runner_path is None:
            # パッケージ内に同梱された bg_runner.js のパスを動的に取得
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            js_runner_path = os.path.join(base_dir, "bg_runner.js")
            
            # ディレクトリ直下に見つからない場合用のフォールバック
            if not os.path.exists(js_runner_path):
                js_runner_path = os.path.join(sys.prefix, "bg_runner.js")

        self.js_runner_path = js_runner_path

    def get_tokens(self) -> Dict[str, str]:
        """バックグラウンドで JS を実行してトークンを取得"""
        if not os.path.exists(self.js_runner_path):
            raise FileNotFoundError(f"JS スクリプトが見つかりません: {self.js_runner_path}")

        try:
            res = subprocess.run(
                ["node", self.js_runner_path],
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(res.stdout)

            if data.get("status") != "success":
                raise RuntimeError(f"トークン生成エラー: {data.get('message')}")

            return {
                "po_token": data["poToken"],
                "visitor_data": data["visitorData"]
            }
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Node.js の実行に失敗しました: {e.stderr}")
        except json.JSONDecodeError:
            raise RuntimeError("JS からの出力結果を JSON として解析できませんでした。")
