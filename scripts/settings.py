"""
Easy Prompt Selector Plus の設定モジュール
"""

from modules import script_callbacks, shared
import traceback

def on_ui_settings():
    """
    UI設定のコールバック関数
    Easy Prompt Selector Plus の設定項目を追加
    """
    try:
        # 設定セクションの定義
        section = "easy_prompt_selector_plus", "Easy Prompt Selector Plus"

        # PNG情報に元プロンプトを保存する設定
        shared.opts.add_option(
            key="eps_enable_save_raw_prompt_to_pnginfo",
            info=shared.OptionInfo(
                False,
                label="元プロンプトを pngninfo に保存する",
                section=section,
            ),
        )

        # タグファイルのパス設定
        shared.opts.add_option(
            key="eps_tags_dir",
            info=shared.OptionInfo(
                "",
                label="タグファイルのパス",
                section=section,
            ),
        )
    except Exception as e:
        print(f"UI設定の追加中にエラーが発生しました: {str(e)}")
        print(traceback.format_exc())

try:
    # UI設定のコールバックを登録
    script_callbacks.on_ui_settings(on_ui_settings)
except Exception as e:
    print(f"UI設定コールバックの登録中にエラーが発生しました: {str(e)}")
    print(traceback.format_exc())
