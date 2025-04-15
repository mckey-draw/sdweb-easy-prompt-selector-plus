/**
 * Easy Prompt Selector Plus - プロンプト選択を簡単にするためのユーティリティクラス
 */

// デバッグ設定の取得
const DEBUG_CONFIG = window.EPS_DEBUG_CONFIG || {
    enabled: false,
    log_level: "INFO",
    show_console: true
};

/**
 * デバッグメッセージを出力
 * @param {string} message - 出力するメッセージ
 */
function debugPrint(message) {
    if (DEBUG_CONFIG.enabled) {
        if (DEBUG_CONFIG.show_console) {
            console.log(`[DEBUG] ${message}`);
        }
    }
}

/**
 * UI要素を構築するためのユーティリティクラス
 */
class EPSElementBuilder {
  /**
   * 基本となるボタン要素を作成
   * @param {string} text - ボタンのテキスト
   * @param {Object} options - ボタンのオプション
   * @param {string} options.size - ボタンのサイズ（'sm'など）
   * @param {string} options.color - ボタンの色（'primary'など）
   * @returns {HTMLElement} 作成されたボタン要素
   */
  static baseButton(text, { size = 'sm', color = 'primary' }) {
    try {
      debugPrint(`ボタン要素を作成します: ${text}`);
      const button = gradioApp().getElementById('txt2img_generate').cloneNode()
      button.id = ''
      button.classList.remove('gr-button-lg', 'gr-button-primary', 'lg', 'primary')
      button.classList.add(
        // gradio 3.16
        `gr-button-${size}`,
        `gr-button-${color}`,
        // gradio 3.22
        size,
        color
      )
      button.textContent = text
      debugPrint(`ボタン要素を作成しました: ${text}`);
      return button
    } catch (error) {
      console.error(`ボタン要素の作成中にエラーが発生しました: ${error.message}`);
      return null;
    }
  }

  /**
   * タグフィールドのコンテナ要素を作成
   * @returns {HTMLElement} 作成されたタグフィールド要素
   */
  static tagFields() {
    const fields = document.createElement('div')
    fields.style.display = 'flex'
    fields.style.flexDirection = 'row'
    fields.style.flexWrap = 'wrap'
    fields.style.minWidth = 'min(320px, 100%)'
    fields.style.maxWidth = '100%'
    fields.style.flex = '1 calc(50% - 20px)'
    fields.style.borderWidth = '1px'
    fields.style.borderColor = 'var(--block-border-color,#374151)'
    fields.style.borderRadius = 'var(--block-radius,8px)'
    fields.style.padding = '8px'
    fields.style.height = 'fit-content'

    return fields
  }

  /**
   * タグ選択を開くためのボタンを作成
   * @param {Object} options - ボタンのオプション
   * @param {Function} options.onClick - クリック時のコールバック関数
   * @returns {HTMLElement} 作成されたボタン要素
   */
  static openButton({ onClick }) {
    const button = EPSElementBuilder.baseButton('🔯タグを選択', { size: 'sm', color: 'secondary' })
    button.classList.add('easy_prompt_selector_plus_button')
    button.addEventListener('click', onClick)

    return button
  }

  /**
   * エリアコンテナ要素を作成
   * @param {string} id - コンテナのID
   * @returns {HTMLElement} 作成されたコンテナ要素
   */
  static areaContainer(id = undefined) {
    try {
      debugPrint(`コンテナ要素を作成します: ${id}`);
      const container = gradioApp().getElementById('txt2img_results').cloneNode()
      container.id = id
      container.style.gap = 0
      container.style.display = 'none'
      debugPrint(`コンテナ要素を作成しました: ${id}`);
      return container
    } catch (error) {
      console.error(`コンテナ要素の作成中にエラーが発生しました: ${error.message}`);
      return null;
    }
  }

  /**
   * タグボタン要素を作成
   * @param {Object} options - ボタンのオプション
   * @param {string} options.title - ボタンのタイトル
   * @param {Function} options.onClick - クリック時のコールバック関数
   * @param {Function} options.onRightClick - 右クリック時のコールバック関数
   * @param {string} options.color - ボタンの色
   * @returns {HTMLElement} 作成されたボタン要素
   */
  static tagButton({ title, onClick, onRightClick, color = 'primary' }) {
    const button = EPSElementBuilder.baseButton(title, { color })
    button.style.height = '2rem'
    button.style.flexGrow = '0'
    button.style.margin = '2px'

    button.addEventListener('click', onClick)
    button.addEventListener('contextmenu', onRightClick)

    return button
  }

  /**
   * ドロップダウン要素を作成
   * @param {string} id - ドロップダウンのID
   * @param {Array} options - 選択肢の配列
   * @param {Object} callbacks - コールバック関数
   * @param {Function} callbacks.onChange - 値変更時のコールバック関数
   * @returns {HTMLElement} 作成されたドロップダウン要素
   */
  static dropDown(id, options, { onChange }) {
    const select = document.createElement('select')
    select.id = id

    // gradio 3.16
    select.classList.add('gr-box', 'gr-input')

    // gradio 3.22
    select.style.color = 'var(--body-text-color)'
    select.style.backgroundColor = 'var(--input-background-fill)'
    select.style.borderColor = 'var(--block-border-color)'
    select.style.borderRadius = 'var(--block-radius)'
    select.style.margin = '2px'
    select.addEventListener('change', (event) => { onChange(event.target.value) })

    const none = ['なし']
    none.concat(options).forEach((key) => {
      const option = document.createElement('option')
      option.value = key
      option.textContent = key
      select.appendChild(option)
    })

    return select
  }

  /**
   * チェックボックス要素を作成
   * @param {string} text - チェックボックスのラベルテキスト
   * @param {Object} callbacks - コールバック関数
   * @param {Function} callbacks.onChange - 値変更時のコールバック関数
   * @returns {HTMLElement} 作成されたチェックボックス要素
   */
  static checkbox(text, { onChange }) {
    const label = document.createElement('label')
    label.style.display = 'flex'
    label.style.alignItems = 'center'

    const checkbox = gradioApp().querySelector('input[type=checkbox]').cloneNode()
    checkbox.checked = false
    checkbox.addEventListener('change', (event) => {
       onChange(event.target.checked)
    })

    const span = document.createElement('span')
    span.style.marginLeft = 'var(--size-2, 8px)'
    span.textContent = text

    label.appendChild(checkbox)
    label.appendChild(span)

    return label
  }
}

/**
 * プロンプト選択のメインクラス
 */
class EasyPromptSelector {
  // 定数定義
  PATH_FILE = 'tmp/easyPromptSelectorPlus.txt'  // 設定ファイルのパス
  AREA_ID = 'easy-prompt-selector-plus'          // メインエリアのID
  SELECT_ID = 'easy-prompt-selector-plus-select' // セレクトボックスのID
  CONTENT_ID = 'easy-prompt-selector-plus-content' // コンテンツエリアのID
  TO_NEGATIVE_PROMPT_ID = 'easy-prompt-selector-plus-to-negative-prompt' // ネガティブプロンプト用のID

  /**
   * コンストラクタ
   * @param {Object} yaml - YAMLパーサー
   * @param {Function} gradioApp - Gradioアプリケーションの参照
   */
  constructor(yaml, gradioApp) {
    this.yaml = yaml
    this.gradioApp = gradioApp
    this.visible = false
    this.toNegative = false
    this.tags = undefined
  }

  /**
   * 初期化処理
   */
  async init() {
    try {
      debugPrint('初期化処理を開始します');
      this.tags = await this.parseFiles()

      const tagArea = gradioApp().querySelector(`#${this.AREA_ID}`)
      if (tagArea != null) {
        this.visible = false
        this.changeVisibility(tagArea, this.visible)
        tagArea.remove()
      }

      gradioApp()
        .getElementById('txt2img_toprow')
        .after(this.render())
      debugPrint('初期化処理が完了しました');
    } catch (error) {
      console.error(`初期化処理中にエラーが発生しました: ${error.message}`);
    }
  }

  /**
   * ファイルを読み込む
   * @param {string} filepath - 読み込むファイルのパス
   * @returns {Promise<string>} ファイルの内容
   */
  async readFile(filepath) {
    try {
      debugPrint(`ファイルを読み込みます: ${filepath}`);
      const response = await fetch(`file=${filepath}?${new Date().getTime()}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const text = await response.text();
      debugPrint(`ファイルを読み込みました: ${filepath}`);
      return text;
    } catch (error) {
      console.error(`ファイル読み込み中にエラーが発生しました (${filepath}): ${error.message}`);
      return '';
    }
  }

  /**
   * 設定ファイルを解析
   * @returns {Promise<Object>} 解析されたタグデータ
   */
  async parseFiles() {
    try {
      debugPrint('設定ファイルの解析を開始します');
      const text = await this.readFile(this.PATH_FILE);
      if (text === '') {
        debugPrint('設定ファイルが空です');
        return {};
      }

      const paths = text.split(/\r\n|\n/);
      const tags = {};

      for (const path of paths) {
        try {
          const filename = path.split('/').pop().split('.').slice(0, -1).join('.');
          const data = await this.readFile(path);
          this.yaml.loadAll(data, function (doc) {
            tags[filename] = doc;
          });
          debugPrint(`タグファイルを解析しました: ${filename}`);
        } catch (error) {
          console.error(`タグファイルの解析中にエラーが発生しました (${path}): ${error.message}`);
        }
      }

      debugPrint(`設定ファイルの解析が完了しました: ${Object.keys(tags).length}ファイル`);
      return tags;
    } catch (error) {
      console.error(`設定ファイルの解析中にエラーが発生しました: ${error.message}`);
      return {};
    }
  }

  /**
   * メインUIのレンダリング
   * @returns {HTMLElement} 作成されたUI要素
   */
  render() {
    const row = document.createElement('div')
    row.style.display = 'flex'
    row.style.alignItems = 'center'
    row.style.gap = '10px'

    const dropDown = this.renderDropdown()
    dropDown.style.flex = '1'
    dropDown.style.minWidth = '1'
    row.appendChild(dropDown)

    const settings = document.createElement('div')
    const checkbox = EPSElementBuilder.checkbox('ネガティブプロンプトに入力', {
      onChange: (checked) => { this.toNegative = checked }
    })
    settings.style.flex = '1'
    settings.appendChild(checkbox)

    row.appendChild(settings)

    const container = EPSElementBuilder.areaContainer(this.AREA_ID)

    container.appendChild(row)
    container.appendChild(this.renderContent())

    return container
  }

  /**
   * ドロップダウンのレンダリング
   * @returns {HTMLElement} 作成されたドロップダウン要素
   */
  renderDropdown() {
    const dropDown = EPSElementBuilder.dropDown(
      this.SELECT_ID,
      Object.keys(this.tags), {
        onChange: (selected) => {
          const content = gradioApp().getElementById(this.CONTENT_ID)
          Array.from(content.childNodes).forEach((node) => {
            const visible = node.id === `easy-prompt-selector-plus-container-${selected}`
            this.changeVisibility(node, visible)
          })
        }
      }
    )

    return dropDown
  }

  /**
   * コンテンツエリアのレンダリング
   * @returns {HTMLElement} 作成されたコンテンツ要素
   */
  renderContent() {
    const content = document.createElement('div')
    content.id = this.CONTENT_ID

    Object.keys(this.tags).forEach((key) => {
      const values = this.tags[key]

      const fields = EPSElementBuilder.tagFields()
      fields.id = `easy-prompt-selector-plus-container-${key}`
      fields.style.display = 'none'
      fields.style.flexDirection = 'row'
      fields.style.marginTop = '10px'

      this.renderTagButtons(values, key).forEach((group) => {
        fields.appendChild(group)
      })

      content.appendChild(fields)
    })

    return content
  }

  /**
   * タグボタンのレンダリング
   * @param {Array|Object} tags - タグデータ
   * @param {string} prefix - タグのプレフィックス
   * @returns {Array<HTMLElement>} 作成されたタグボタン要素の配列
   */
  renderTagButtons(tags, prefix = '') {
    if (Array.isArray(tags)) {
      return tags.map((tag) => this.renderTagButton(tag, tag, 'secondary'))
    } else {
      return Object.keys(tags).map((key) => {
        const values = tags[key]
        const randomKey = `${prefix}:${key}`

        if (typeof values === 'string') { return this.renderTagButton(key, values, 'secondary') }

        const fields = EPSElementBuilder.tagFields()
        fields.style.flexDirection = 'column'

        fields.append(this.renderTagButton(key, `@${randomKey}@`))

        const buttons = EPSElementBuilder.tagFields()
        buttons.id = 'buttons'
        fields.append(buttons)
        this.renderTagButtons(values, randomKey).forEach((button) => {
          buttons.appendChild(button)
        })

        return fields
      })
    }
  }

  renderTagButton(title, value, color = 'primary') {
    return EPSElementBuilder.tagButton({
      title,
      onClick: (e) => {
        e.preventDefault();

        this.addTag(value, this.toNegative || e.metaKey || e.ctrlKey)
      },
      onRightClick: (e) => {
        e.preventDefault();

        this.removeTag(value, this.toNegative || e.metaKey || e.ctrlKey)
      },
      color
    })
  }

  /**
   * タグボタンの表示/非表示を切り替え
   * @param {HTMLElement} node - 対象の要素
   * @param {boolean} visible - 表示/非表示のフラグ
   */
  changeVisibility(node, visible) {
    node.style.display = visible ? 'flex' : 'none'
  }

  /**
   * タグを追加
   * @param {string} tag - 追加するタグ
   * @param {boolean} toNegative - ネガティブプロンプトに追加するかどうか
   */
  addTag(tag, toNegative = false) {
    const id = toNegative ? 'txt2img_neg_prompt' : 'txt2img_prompt'
    const textarea = gradioApp().getElementById(id).querySelector('textarea')

    if (textarea.value.trim() === '') {
      textarea.value = tag
    } else if (textarea.value.trim().endsWith(',')) {
      textarea.value += ' ' + tag
    } else {
      textarea.value += ', ' + tag
    }

    updateInput(textarea)
  }

  /**
   * タグを削除
   * @param {string} tag - 削除するタグ
   * @param {boolean} toNegative - ネガティブプロンプトから削除するかどうか
   */
  removeTag(tag, toNegative = false) {
    const id = toNegative ? 'txt2img_neg_prompt' : 'txt2img_prompt'
    const textarea = gradioApp().getElementById(id).querySelector('textarea')

    if (textarea.value.trimStart().startsWith(tag)) {
      const matched = textarea.value.match(new RegExp(`${tag.replace(/[-\/\\^$*+?.()|\[\]{}]/g, '\\$&') },*`))
      textarea.value = textarea.value.replace(matched[0], '').trimStart()
    } else {
      textarea.value = textarea.value.replace(`, ${tag}`, '')
    }

    updateInput(textarea)
  }
}

onUiLoaded(async () => {
  try {
    debugPrint('UIの読み込みが完了しました');
    yaml = window.jsyaml
    const easyPromptSelector = new EasyPromptSelector(yaml, gradioApp())

    const button = EPSElementBuilder.openButton({
      onClick: () => {
        const tagArea = gradioApp().querySelector(`#${easyPromptSelector.AREA_ID}`)
        easyPromptSelector.changeVisibility(tagArea, easyPromptSelector.visible = !easyPromptSelector.visible)
      }
    })

    const reloadButton = gradioApp().getElementById('easy_prompt_selector_plus_reload_button')
    if (reloadButton) {
      reloadButton.addEventListener('click', async () => {
        try {
          await easyPromptSelector.init()
          debugPrint('タグの再読み込みが完了しました');
        } catch (error) {
          console.error(`タグの再読み込み中にエラーが発生しました: ${error.message}`);
        }
      })
    }

    const txt2imgActionColumn = gradioApp().getElementById('txt2img_actions_column')
    if (txt2imgActionColumn) {
      const container = document.createElement('div')
      container.classList.add('easy_prompt_selector_plus_container')
      container.appendChild(button)
      if (reloadButton) {
        container.appendChild(reloadButton)
      }
      txt2imgActionColumn.appendChild(container)
    }

    await easyPromptSelector.init()
    debugPrint('初期化が完了しました');
  } catch (error) {
    console.error(`UIの初期化中にエラーが発生しました: ${error.message}`);
    console.error(error.stack);
  }
}) 