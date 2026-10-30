# 文書を作る道具

| ファイル | 役割 |
|---|---|
| `definition.py` | データ定義書（Excel）の読み書きと点検。`dump`（Excel → JSON）・`build`（JSON → 新しい版の Excel）・`check`（点検）・`new`（空の JSON） |
| `deck_lib.py` | pptx を作る部品（`Deck`・`slide`・`text`・`box`・`table`・`line`）。テンプレートがあれば `Deck(..., template=...)` |
| `render_pptx.py` | pptx を PowerPoint（COM）で PNG にする。`python doc_tools/render_pptx.py "docs/….pptx" [ページ]` |
| `check_env.py` | 上の道具が動く環境かを確かめる（Excel・PowerPoint を使う） |
| `examples/` | 手本。`sample_definition.json` はサンプルの定義書の元、`guide_deck.py` は deck_lib で説明資料を作る例 |
| `work/` | 変更ごとのスクリプトの置き場（Git に入れない） |
| `render/` | PNG の書き出し先（Git に入れない） |

## 準備（初回だけ）
```
python -m pip install -r doc_tools/requirements.txt
python doc_tools/check_env.py
```

## データ定義書の直し方
```
python doc_tools/definition.py dump  "docs/【データ定義書】…_v0.1.xlsx" doc_tools/work/def.json
（def.json を直す）
python doc_tools/definition.py build doc_tools/work/def.json "docs/【データ定義書】…_v0.2.xlsx"
python doc_tools/definition.py check "docs/【データ定義書】…_v0.2.xlsx"
```
確かめたら古い版を docs/ から消す。JSON の形は `examples/sample_definition.json`、型・層の一覧は定義書の 00_凡例。
