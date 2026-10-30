# AI への指示

GitHub Copilot はこのファイルを自動で読む。Claude Code は CLAUDE.md、そのほかの AI は AGENTS.md から、このファイルを読む。

## 共通
- 回答・コメント・コミットメッセージは日本語で書く。作業が長く続いても英語に切り替えない
- 作業の前に `rules/README.md`（作業ルールの索引）を読み、関係するルールを本文まで読む。新しい資料・設計に入るときは `rules/` を全件と `rules/project/` を読んでから構成を決める
- 進め方は `playbook/README.md` の段階に従う。段階を飛ばさない（とくに、事象と課題、To-Be像が決まる前にデータモデルを書かない）
- 次のことは作る前にユーザーに確かめる：実現したいこと（To-Be像）、データモデルの範囲と1行の単位、判定の閾値・信号の色、資料の構成、ファイルの削除。メールなど外部への送信はしない（下書きまで）
- ユーザーの指摘は、理由とあわせて `rules/`（どのプロジェクトでも効くもの）か `rules/project/`（このプロジェクトだけ）に書き、索引に1行足す
- 作業の終わりに `python check_all.py` を流し、結果をそのまま報告する。NG を OK と言わない

## リポジトリの構成
- `docs/`：プロジェクトの文書の最新版（データ定義書・説明資料・検討メモ）。各文書1つだけ置く
- `doc_tools/`：文書を作る道具（`doc_tools/README.md`）
- `app/`：試作アプリ（Django・SQLite。`app/README.md`）
- `rules/`：作業ルール。`playbook/`：進め方の手順書

## 文書（docs/）
- 文書は直接手で編集せず、変更ごとに Python のスクリプトを `doc_tools/work/` に書いて作る。版を上げるときは新しい版のファイルを作り、元の版は上書きしない。スクリプトの冒頭で「出力先が既にあれば止める」assert を入れる
- データ定義書は `doc_tools/definition.py` で作る（dump → JSON を直す → build）。作ったら `definition.py check` で誤り 0 件にする
- pptx は `doc_tools/deck_lib.py` で作り、`doc_tools/render_pptx.py` で PNG にして全ページを見る
- 人が作った Excel は Excel COM で編集し、openpyxl は読むだけにする（`rules/excel-com.md`）
- 文章は `rules/business-doc-writing.md`、構成は `rules/doc-structure.md`、体裁は `rules/pptx-format.md` に従う

## アプリ（app/）
- コマンドは `app/` で実行する。Python 3.12 以上、Django 6.1、SQLite（`app/app.db`）
- 領域ごとのアプリ（`core/apps.json` に並ぶもの）は `tools/gen_models.py` がデータ定義書から生成したもの。直接編集せず、データ定義書を直して `python tools/rebuild.py` で作り直す
- 業務画面は `work/` に置く。計算は `work/<業務>.py` の関数、画面は `views_<業務>.py`、メニューは `work/nav.py`。手本は `work/sample.py`
- 判定の閾値・目標値はマスタから読み、コードに数値を直書きしない（仮置きするときはコメントを残し、定義書の不足として一覧にする）
- 金額は百万円・小数2桁（単価は円）。テンプレートでは `{% load fmt %}` の `mil`・`num`
- 画面の文言は体言止め・あいまい語なし（`tools/audit_wording.py` で点検）
- 手元で動かす試作。ログインなしの業務画面と `/admin/`（admin／admin）だけ。本番向けの設定（認証、SECRET_KEY など）は求められない限り足さない
