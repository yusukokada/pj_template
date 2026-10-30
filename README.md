# プロジェクトのひな型

データモデルを考え、データ定義書を作り、試作アプリを組み立て、業務の画面と説明資料にするまでを、AI（GitHub Copilot・Claude Code など）と進めるためのひな型。

どの AI でも同じ手順・同じ確かめ方で進められるように、次の4つを揃えてある。
- **ルール**（`rules/`）：資料の書き方・データモデルの考え方・画面の作り方。これまでの指摘を理由つきでまとめたもの
- **手順書**（`playbook/`）：段階ごとに、作るもの・確かめ方・ユーザーに確かめること・次へ進む条件
- **決まった道具**：データ定義書の読み書き（`doc_tools/definition.py`）、定義書からのアプリの生成（`app/tools/gen_models.py`）、pptx の部品（`doc_tools/deck_lib.py`）
- **確かめる道具**：定義書の点検、全画面の確認、文言の点検、pptx の PNG 書き出し。まとめて `python check_all.py`

サンプルとして、小さな案件管理の定義書（6テーブル）と、そこから生成したアプリ、業務画面の手本（案件の状況）が入っている。

| フォルダ | 中身 |
|---|---|
| `docs/` | 文書の最新版（いまはサンプルの定義書だけ） |
| `doc_tools/` | 文書を作る道具（`doc_tools/README.md`） |
| `app/` | 試作アプリ（`app/README.md`） |
| `rules/` | 作業ルール（索引は `rules/README.md`）。プロジェクト固有のものは `rules/project/` |
| `playbook/` | 進め方の手順書 |
| `guide/` | このひな型の説明資料（立上げ方・進め方・人が押さえるポイント、ITマネジメント高度化での実物と依頼の型、15枚）。プロジェクト計画書と同じ ITPMテンプレ.pptx の体裁。作り方は `doc_tools/examples/guide_deck.py`（テンプレートのパスを渡して実行） |
| `.github/copilot-instructions.md` | AI への指示（Claude Code は `CLAUDE.md`、そのほかは `AGENTS.md` から読む） |

## 準備
```
python -m pip install -r doc_tools/requirements.txt -r app/requirements.txt
python check_all.py
```
すべて OK なら使える。Excel・PowerPoint の無い環境では `python check_all.py --no-office`。

## 新しいプロジェクトの始め方
1. このひな型から新しいリポジトリを作る（GitHub の「Use this template」か、フォルダごと写す）
2. この README の表題と説明を、プロジェクトのものに書き換える
3. `app/work/nav.py` の SYSTEM_NAME をシステムの名前にする
4. AI に「`playbook/README.md` に沿って、1. 事象と課題 から始めたい。テーマは〜」と頼む
5. 自分のデータ定義書ができたら、サンプルの定義書（docs/）と業務画面の手本（`app/work/` の sample）を消す

## ひな型を育てる
プロジェクトで受けた指摘のうち、どのプロジェクトでも効くものは、ひな型の `rules/` にも戻す。道具の改良も同じ。
