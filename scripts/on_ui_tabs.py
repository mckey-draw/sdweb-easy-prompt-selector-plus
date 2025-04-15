import os
import gradio as gr
import traceback
import yaml
from pathlib import Path

from modules import script_callbacks
from scripts.setup import get_tag_files, get_tags_dir
from scripts.configs import config, debug_print

def validate_yaml(content):
    """
    YAML形式のバリデーションを行う
    Args:
        content (str): バリデーション対象の文字列
    Returns:
        tuple: (bool, str) - (バリデーション結果, エラーメッセージ)
    """
    try:
        yaml.safe_load(content)
        return True, ""
    except yaml.YAMLError as e:
        if config["debug"]["enabled"]:
            print(f"YAMLバリデーションエラー: {str(e)}")
        return False, str(e)

def load_tag_file_content(tag_file_name):
    """
    タグファイルの内容を読み込む
    Args:
        tag_file_name (str): タグファイル名
    Returns:
        str: タグファイルの内容
    """
    try:
        for file in get_tag_files():
            if file.stem == tag_file_name:
                with open(file, "r", encoding="utf-8") as f:
                    return f.read()
        return ""
    except Exception as e:
        print(f"タグファイルの読み込み中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())
        return ""

def save_tag_file_content(tag_file_name, content):
    """
    タグファイルの内容を保存する
    Args:
        tag_file_name (str): タグファイル名
        content (str): 保存する内容
    Returns:
        str: 保存結果のメッセージ
    """
    try:
        for file in get_tag_files():
            if file.stem == tag_file_name:
                with open(file, "w", encoding="utf-8") as f:
                    f.write(content)
                if config["debug"]["enabled"]:
                    print(f"ファイルを保存しました: {file}")
                return "保存しました"
        return "ファイルが見つかりません"
    except Exception as e:
        error_msg = f"タグファイルの保存中にエラーが発生しました: {str(e)}"
        if config["debug"]["enabled"]:
            print(error_msg)
            print(traceback.format_exc())
        return f"エラー: {str(e)}"

def create_new_tag_file(file_name):
    """
    新しいタグファイルを作成する
    Args:
        file_name (str): 作成するファイル名
    Returns:
        tuple: (成功/失敗のメッセージ, 更新されたタグファイルリスト)
    """
    try:
        # ファイル名の重複チェック
        for file in get_tag_files():
            if file.stem == file_name:
                return "同じ名前のファイルが既に存在します", None

        # 新しいファイルを作成
        new_file = get_tags_dir() / f"{file_name}.yml"
        with open(new_file, "w", encoding="utf-8") as f:
            f.write("")

        # 更新されたタグファイルリストを取得
        tag_files = [str(file.stem) for file in get_tag_files()]
        return "ファイルを作成しました", tag_files
    except Exception as e:
        print(f"タグファイルの作成中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())
        return f"エラー: {str(e)}", None

# コンポーネントを作成
def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        # デバッグ設定をHTMLに埋め込む
        gr.HTML(f"""
            <script>
                window.EPS_DEBUG_CONFIG = {{
                    enabled: {str(config["debug"]["enabled"]).lower()}
                }};
            </script>
        """)

        with gr.Row():
            # タグファイルのドロップダウンを作成
            tag_files = []
            for file in get_tag_files():
                # タグディレクトリからの相対パスを取得
                rel_path = file.relative_to(get_tags_dir())
                # サブディレクトリ名を含めた表示名を作成
                display_name = str(rel_path.parent / rel_path.stem) if rel_path.parent != Path('.') else rel_path.stem
                tag_files.append((display_name, str(file.stem)))
            
            tag_dropdown = gr.Dropdown(
                choices=tag_files,
                label="タグファイル選択",
                value="",
                interactive=True
            )

            # 保存ボタンと新規作成ボタンを同じ行に配置
            save_button = gr.Button("保存", variant="primary", size="sm")
            new_button = gr.Button("新規作成", variant="secondary", size="sm")

        # タグファイルの内容を表示するテキストボックスを新しい行に配置
        tag_content = gr.Textbox(
            label="タグファイルの内容",
            lines=20,
            interactive=True
        )

        # 新規作成用のモーダルウィンドウ
        with gr.Column(visible=False) as modal:
            gr.Markdown("### 新しいタグファイルの作成")
            with gr.Row():
                new_file_dir = gr.Textbox(
                    label="サブディレクトリ名（オプション）",
                    placeholder="",
                    interactive=True
                )
            with gr.Row():
                new_file_name = gr.Textbox(
                    label="新しいタグファイル名",
                    placeholder="ファイル名を入力してください",
                    interactive=True
                )
            with gr.Row():
                cancel_button = gr.Button("キャンセル", variant="secondary")
                ok_button = gr.Button("OK", variant="primary")
            modal_result = gr.Textbox(
                label="結果",
                interactive=False,
                visible=False
            )

        # ドロップダウンの選択変更時にテキストボックスの内容を更新
        tag_dropdown.change(
            fn=load_tag_file_content,
            inputs=[tag_dropdown],
            outputs=[tag_content]
        )

        # 保存ボタンクリック時にファイルを保存
        def save_with_validation(tag_file_name, content):
            is_valid, error_message = validate_yaml(content)
            if not is_valid:
                gr.Info(f"YAML形式が正しくありません: {error_message}")
                return
            
            result = save_tag_file_content(tag_file_name, content)
            if result == "保存しました":
                gr.Info("保存が完了しました")
            else:
                gr.Info(f"保存に失敗しました: {result}")

        save_button.click(
            fn=save_with_validation,
            inputs=[tag_dropdown, tag_content],
            outputs=[]
        )

        # 新規作成ボタンクリック時にモーダルを表示
        def show_modal():
            return gr.update(visible=True)
        new_button.click(
            fn=show_modal,
            outputs=[modal]
        )

        # キャンセルボタンクリック時にモーダルを非表示
        def hide_modal():
            return gr.update(visible=False)
        cancel_button.click(
            fn=hide_modal,
            outputs=[modal]
        )

        # OKボタンクリック時にファイルを作成
        def create_file(dir_name, file_name):
            try:
                # サブディレクトリのパスを作成
                if dir_name:
                    dir_path = get_tags_dir() / dir_name
                    dir_path.mkdir(parents=True, exist_ok=True)
                    new_file = dir_path / f"{file_name}.yml"
                else:
                    new_file = get_tags_dir() / f"{file_name}.yml"

                # ファイル名の重複チェック
                if new_file.exists():
                    return {
                        modal: gr.update(visible=True),
                        modal_result: "同じ名前のファイルが既に存在します"
                    }

                # 新しいファイルを作成
                with open(new_file, "w", encoding="utf-8") as f:
                    f.write("")

                # 更新されたタグファイルリストを取得
                tag_files = []
                for file in get_tag_files():
                    rel_path = file.relative_to(get_tags_dir())
                    display_name = str(rel_path.parent / rel_path.stem) if rel_path.parent != Path('.') else rel_path.stem
                    tag_files.append((display_name, str(file.stem)))

                return {
                    modal: gr.update(visible=False),
                    tag_dropdown: gr.update(choices=tag_files, value=file_name),
                    modal_result: "ファイルを作成しました"
                }
            except Exception as e:
                error_msg = f"タグファイルの作成中にエラーが発生しました: {str(e)}"
                if config["debug"]["enabled"]:
                    print(error_msg)
                    print(traceback.format_exc())
                return {
                    modal: gr.update(visible=True),
                    modal_result: error_msg
                }

        ok_button.click(
            fn=create_file,
            inputs=[new_file_dir, new_file_name],
            outputs=[modal, tag_dropdown, modal_result]
        )

    return [(ui_component, "Easy Prompt Selector", "easy_propmt_selector_tab")]

# 作成したコンポーネントをwebuiに登録
try:
    script_callbacks.on_ui_tabs(on_ui_tabs)
except Exception as e:
    print(f"UI設定コールバックの登録中にエラーが発生しました: {str(e)}")
    print(traceback.format_exc())
