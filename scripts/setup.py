"""
Easy Prompt Selector Plus のセットアップモジュール
タグファイルの初期化と管理を行う
"""

from pathlib import Path
import shutil
import os
import traceback

from modules.scripts import basedir

# ディレクトリパスの定義
FILE_DIR = Path().absolute()  # 現在のディレクトリ
BASE_DIR = Path(basedir())    # ベースディレクトリ
TEMP_DIR = FILE_DIR.joinpath('tmp')  # 一時ファイルディレクトリ

# タグ関連のディレクトリ
TAGS_DIR = BASE_DIR.joinpath('tags')  # タグファイルディレクトリ
EXAMPLES_DIR = BASE_DIR.joinpath('tags_examples')  # サンプルタグディレクトリ

# ファイル名の定義
FILENAME_LIST = 'easyPromptSelectorPlus.txt'

def create_directories():
    """
    必要なディレクトリを作成
    """
    try:
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.makedirs(TAGS_DIR, exist_ok=True)
        os.makedirs(EXAMPLES_DIR, exist_ok=True)
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
        for file in examples():
            try:
                file_path = str(file).replace('tags_examples', 'tags')
                shutil.copy2(file, file_path)
            except Exception as e:
                print(f"ファイルコピー中にエラーが発生しました ({file}): {str(e)}")
    except Exception as e:
        print(f"サンプルタグコピー中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())

def tags():
    """
    タグファイルのパスを取得
    Returns:
        Generator: タグファイルのパス
    """
    try:
        return TAGS_DIR.rglob("*.yml")
    except Exception as e:
        print(f"タグファイルの取得中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())
        return []

def write_filename_list():
    """
    タグファイルのリストを一時ファイルに書き出し
    """
    try:
        filepaths = map(lambda path: path.relative_to(FILE_DIR).as_posix(), list(tags()))

        with open(TEMP_DIR.joinpath(FILENAME_LIST), 'w', encoding="utf-8") as f:
            f.write('\n'.join(sorted(filepaths)))
    except Exception as e:
        print(f"ファイルリスト書き出し中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())

# メイン処理
try:
    # ディレクトリの作成
    create_directories()

    # タグファイルが存在しない場合はサンプルをコピー
    if len(list(TAGS_DIR.rglob("*.yml"))) == 0:
        copy_examples()

    # タグファイルリストの作成
    write_filename_list()
except Exception as e:
    print(f"セットアップ処理中にエラーが発生しました: {str(e)}")
    print(traceback.format_exc())
