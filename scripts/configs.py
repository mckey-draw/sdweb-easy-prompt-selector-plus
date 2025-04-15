"""
Easy Prompt Selector Plus の設定管理モジュール
設定ファイルの読み込みとデバッグ設定の管理を行う
"""

import json
from pathlib import Path
import modules.scripts as scripts

# 設定ファイルの読み込み
def load_config():
    """
    設定ファイルを読み込む
    Returns:
        dict: 設定データ
    """
    config_path = Path(scripts.basedir()) / "config.json"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config
    except Exception as e:
        print(f"設定ファイルの読み込みに失敗しました: {str(e)}")
        return {"debug": {"enabled": False}}

# デバッグ設定の読み込み
config = load_config()

def debug_print(message):
    """
    デバッグメッセージを出力
    Args:
        message (str): 出力するメッセージ
    """
    if config["debug"]["enabled"]:
        print(f"[DEBUG] {message}") 