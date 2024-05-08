matagpt：https://github.com/geekan/MetaGPT?tab=readme-ov-file#contact-information

このリポジトリはmetagptの日本語化を試すリポジトリです。
- プロンプト文の日本語化
- 日本語に適したアルゴリズムの変更や対応など
- 日本語用openLLMに適した処理の方法 + ハルシネーションの検知などを目指します
    - api系LLMの場合はほとんどの場合で日本語と英語が対応可能なので日本語用openLLMに目的を合わせます

## 日本語化進捗（確認済みを記載）
- プロンプトが含まれるコードがある場合は以下の流れを踏襲
    - issueをファイル名をタイトルとして立てる
    - 対象コードの情報（行数、実際のコードなど）を記載
    - deepLなどのツールによる単純翻訳を載せる
    - プロンプトをローカルLLMで最大限動かせるように変更（例えば日英の単純和訳だと小数点以下の扱いなどが損なわれやすいためそこを修正など）
    - 変更後のプロンプトを載せる

ローカルLLMの利用方法によっては日本語化しきらない場合のほうが良いこともあるので元のpromptも残す。
<details close><summary>src/metagpt/actions</summary>


- init.py
- action_graph.py
- action_node.py
- action_outcls_registry.py
- action_output.py

</details>
