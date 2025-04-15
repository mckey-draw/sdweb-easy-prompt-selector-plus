"""
Easy Prompt Selector Plus のセットアップモジュール
タグファイルの初期化と管理を行う
"""

from pathlib import Path
import shutil
import os
import traceback

from modules import scripts
from modules import shared
from scripts.configs import config, debug_print

# ディレクトリパスの定義
BASE_DIR = Path(scripts.basedir())  # ベースディレクトリ
TEMP_DIR = Path().joinpath('tmp')  # 一時ファイルディレクトリ

# タグ関連のディレクトリ
DEF_TAGS_DIR = BASE_DIR.joinpath('tags')  # デフォルトタグファイルディレクトリ
EXAMPLES_DIR = BASE_DIR.joinpath('tags_examples')  # サンプルタグディレクトリ

# ファイル名の定義
FILENAME_LIST = 'easyPromptSelectorPlus.txt'

def create_directories():
    """
    必要なディレクトリを作成
    """
    try:
        debug_print("ディレクトリ作成を開始します")
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.makedirs(DEF_TAGS_DIR, exist_ok=True)
        debug_print(f"一時ディレクトリ: {TEMP_DIR}")
        debug_print(f"タグディレクトリ: {DEF_TAGS_DIR}")
    except Exception as e:
        print(f"ディレクトリ作成中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())

def examples():
    """
    サンプルタグファイルのパスを取得
    Returns:
        Generator: サンプルタグファイルのパス
    """
    try:
        debug_print("サンプルタグファイルの取得を開始します")
        return EXAMPLES_DIR.rglob("*.yml")
    except Exception as e:
        print(f"サンプルタグファイルの取得中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())
        return []

def copy_examples():
    """
    サンプルタグファイルをタグディレクトリにコピー
    """
    try:
        debug_print("サンプルタグファイルのコピーを開始します")
        for file in examples():
            try:
                # Pathオブジェクトを使用して安全にパスを生成
                target_path = DEF_TAGS_DIR.joinpath(file.relative_to(EXAMPLES_DIR))
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, target_path)
                debug_print(f"ファイルをコピーしました: {file} -> {target_path}")
            except Exception as e:
                print(f"ファイルコピー中にエラーが発生しました ({file}): {str(e)}")
                print(traceback.format_exc())
    except Exception as e:
        print(f"サンプルタグコピー中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())

def get_tags_dir():
    """
    タグファイルのディレクトリを取得
    Returns:
        Path: タグファイルのディレクトリ
    """
    try:
        opt_dir = Path(shared.opts.eps_tags_dir)
        tags_dir = opt_dir if opt_dir != Path("") else DEF_TAGS_DIR
        debug_print(f"eps_tags_dir: {tags_dir}")
        return tags_dir
    except Exception as e:
        print(f"タグディレクトリの取得中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())
        return DEF_TAGS_DIR

def get_tag_files():
    """
    タグファイルのパスを取得
    Returns:
        Generator: タグファイルのパス
    """
    try:
        debug_print("タグファイルの取得を開始します")
        return get_tags_dir().rglob("*.yml")
    except Exception as e:
        print(f"タグファイルの取得中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())
        return []

def write_filename_list():
    """
    タグファイルのリストを一時ファイルに書き出し
    """
    try:
        debug_print("ファイルリストの書き出しを開始します")
        filepaths = []
        for path in get_tag_files():
            try:
                # フルパスを使用
                filepaths.append(str(path))
            except ValueError as e:
                print(f"パス変換中にエラーが発生しました ({path}): {str(e)}")
                continue

        with open(TEMP_DIR.joinpath(FILENAME_LIST), 'w', encoding="utf-8") as f:
            f.write('\n'.join(sorted(filepaths)))
        debug_print(f"ファイルリストを書き出しました: {TEMP_DIR.joinpath(FILENAME_LIST)}")
    except Exception as e:
        print(f"ファイルリスト書き出し中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())

# メイン処理
try:
    debug_print("セットアップ処理を開始します")
    
    # ディレクトリの作成
    create_directories()

    # タグファイルが存在しない場合はサンプルをコピー
    if len(list(get_tags_dir().rglob("*.yml"))) == 0:
        copy_examples()

    # タグファイルリストの作成
    write_filename_list()
    
    debug_print("セットアップ処理が完了しました")
except Exception as e:
    print(f"セットアップ処理中にエラーが発生しました: {str(e)}")
    print(traceback.format_exc())
