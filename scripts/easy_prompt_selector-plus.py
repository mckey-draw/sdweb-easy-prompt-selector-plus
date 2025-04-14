"""
Easy Prompt Selector Plus のメインスクリプト
プロンプトのテンプレート処理とタグ管理を行う
"""

from pathlib import Path
import random
import re
import yaml
import gradio as gr
import traceback

import modules.scripts as scripts
from modules.scripts import AlwaysVisible, basedir
from modules import shared
from scripts.setup import write_filename_list

# ディレクトリパスの定義
FILE_DIR = Path().absolute()  # 現在のディレクトリ
BASE_DIR = Path(basedir())    # ベースディレクトリ
TAGS_DIR = BASE_DIR.joinpath('tags')  # タグファイルディレクトリ

def tag_files():
    """
    タグファイルのパスを取得
    Returns:
        Generator: タグファイルのパス
    """
    print(f"TAGS_DIR:{TAGS_DIR}")
    try:
        return TAGS_DIR.rglob("*.yml")
    except Exception as e:
        print(f"タグファイルの取得中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())
        return []

def load_tags():
    """
    タグファイルを読み込む
    Returns:
        dict: 読み込まれたタグデータ
    """
    tags = {}
    try:
        for filepath in tag_files():
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    yml = yaml.safe_load(file)
                    if yml is None:
                        print(f"警告: {filepath} は空のファイルです")
                        continue
                    tags[filepath.stem] = yml
            except yaml.YAMLError as e:
                print(f"YAML解析エラー ({filepath}): {str(e)}")
            except Exception as e:
                print(f"ファイル読み込みエラー ({filepath}): {str(e)}")
    except Exception as e:
        print(f"タグ読み込み中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())
    return tags

def find_tag(tags, location):
    """
    タグを検索する
    Args:
        tags (dict): タグデータ
        location (str or list): タグの位置
    Returns:
        str: 見つかったタグの値
    """
    try:
        if type(location) == str:
            return tags[location]

        value = ''
        if len(location) > 0:
            value = tags
            for tag in location:
                value = value[tag]

        if type(value) == dict:
            key = random.choice(list(value.keys()))
            tag = value[key]
            if type(tag) == dict:
                value = find_tag(tag, [random.choice(list(tag.keys()))])
            else:
                value = find_tag(value, key)

        if (type(value) == list):
            value = random.choice(value)

        return value
    except Exception as e:
        print(f"タグ検索中にエラーが発生しました (location: {location}): {str(e)}")
        return ""

def replace_template(tags, prompt, seed = None):
    """
    プロンプト内のテンプレートを置換する
    Args:
        tags (dict): タグデータ
        prompt (str): プロンプトテキスト
        seed (int, optional): 乱数シード
    Returns:
        str: 置換後のプロンプト
    """
    try:
        random.seed(seed)

        count = 0
        while count < 100:
            if not '@' in prompt:
                break

            for match in re.finditer(r'(@((?P<num>\d+(-\d+)?)\$\$)?(?P<ref>[^>]+?)@)', prompt):
                template = match.group()
                try:
                    try:
                        result = list(map(lambda x: int(x), match.group('num').split('-')))
                        min_count = min(result)
                        max_count = max(result)
                    except Exception as e:
                        min_count, max_count = 1, 1
                    count = random.randint(min_count, max_count)

                    values = list(map(lambda x: find_tag(tags, match.group('ref').split(':')), list(range(count))))
                    prompt = prompt.replace(template, ', '.join(values), 1)
                except Exception as e:
                    print(f"テンプレート置換中にエラーが発生しました (template: {template}): {str(e)}")
                    prompt = prompt.replace(template, '', 1)
            count += 1

        random.seed()
        return prompt
    except Exception as e:
        print(f"プロンプト置換中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())
        return prompt

class Script(scripts.Script):
    """
    Easy Prompt Selector Plus のメインスクリプトクラス
    """
    tags = {}

    def __init__(self):
        """
        初期化処理
        """
        try:
            super().__init__()
            self.tags = load_tags()
        except Exception as e:
            print(f"スクリプト初期化中にエラーが発生しました: {str(e)}")
            print(traceback.format_exc())
            self.tags = {}

    def title(self):
        """
        スクリプトのタイトルを返す
        Returns:
            str: スクリプトのタイトル
        """
        return "EasyPromptSelector"

    def show(self, is_img2img):
        """
        スクリプトの表示設定
        Args:
            is_img2img (bool): img2imgモードかどうか
        Returns:
            AlwaysVisible: 常に表示する
        """
        return AlwaysVisible

    def ui(self, is_img2img):
        """
        UIの構築
        Args:
            is_img2img (bool): img2imgモードかどうか
        Returns:
            list: UI要素のリスト
        """
        try:
            if (is_img2img):
                return None

            # リロードボタンの作成
            reload_button = gr.Button('🔄', variant='secondary', elem_id='easy_prompt_selector_reload_button')
            reload_button.style(size='sm')

            def reload():
                """
                タグの再読み込み
                """
                try:
                    self.tags = load_tags()
                    write_filename_list()
                except Exception as e:
                    print(f"タグ再読み込み中にエラーが発生しました: {str(e)}")
                    print(traceback.format_exc())

            reload_button.click(fn=reload)

            return [reload_button]
        except Exception as e:
            print(f"UI構築中にエラーが発生しました: {str(e)}")
            print(traceback.format_exc())
            return None

    def replace_template_tags(self, p):
        """
        プロンプト内のテンプレートタグを置換
        Args:
            p: プロンプトパラメータ
        """
        try:
            prompts = [
                [p.prompt, p.all_prompts, 'Input Prompt'],
                [p.negative_prompt, p.all_negative_prompts, 'Input NegativePrompt'],
            ]
            if getattr(p, 'hr_prompt', None): prompts.append([p.hr_prompt, p.all_hr_prompts, 'Input Prompt(Hires)'])
            if getattr(p, 'hr_negative_prompt', None): prompts.append([p.hr_negative_prompt, p.all_hr_negative_prompts, 'Input NegativePrompt(Hires)'])

            for i in range(len(p.all_prompts)):
                seed = random.random()
                for [prompt, all_prompts, raw_prompt_param_name] in prompts:
                    if '@' not in prompt: continue

                    self.save_prompt_to_pnginfo(p, prompt, raw_prompt_param_name)

                    replaced = "".join(replace_template(self.tags, all_prompts[i], seed))
                    all_prompts[i] = replaced
        except Exception as e:
            print(f"テンプレートタグ置換中にエラーが発生しました: {str(e)}")
            print(traceback.format_exc())

    def save_prompt_to_pnginfo(self, p, prompt, name):
        """
        PNG情報にプロンプトを保存
        Args:
            p: プロンプトパラメータ
            prompt (str): プロンプトテキスト
            name (str): パラメータ名
        """
        try:
            if shared.opts.eps_enable_save_raw_prompt_to_pnginfo == False:
                return

            p.extra_generation_params.update({name: prompt.replace('\n', ' ')})
        except Exception as e:
            print(f"PNG情報保存中にエラーが発生しました: {str(e)}")
            print(traceback.format_exc())

    def process(self, p, *args):
        """
        プロンプトの処理
        Args:
            p: プロンプトパラメータ
            *args: その他の引数
        """
        try:
            self.replace_template_tags(p)
        except Exception as e:
            print(f"プロンプト処理中にエラーが発生しました: {str(e)}")
            print(traceback.format_exc())
