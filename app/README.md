# 試作アプリ

データ定義書から生成する、手元で動かす試作（Python・Django・SQLite）。

## 動かす
```
cd app
python -m pip install -r requirements.txt
python manage.py runserver        （または start.bat）
```
http://127.0.0.1:8000 を開く。`/admin/` はテーブル単位の管理画面（admin／admin）。

## 作り直す（データ定義書を直したとき）
```
python tools/rebuild.py           （docs/ の【データ定義書】から生成 → DB を作り直し → ダミーデータ）
python tools/smoke.py             （全画面が開くか）
python tools/audit_wording.py     （画面の文言の点検）
```

## ファイルの役割
| 場所 | 中身 | 直してよいか |
|---|---|---|
| `core/apps.json` に並ぶフォルダ（サンプルでは master・prj・metric） | 領域ごとのモデルと管理画面 | 直さない（`tools/gen_models.py` が生成） |
| `core/schema.json`・`codes.json` | 生成したテーブル・項目・選択肢の一覧（ダミーデータ・smoke が使う） | 直さない |
| `core/admin_base.py` | 管理画面の共通の設定（導出のテーブルは編集不可など） | 直してよい |
| `core/management/commands/seed.py` | どの定義書でも動く乱数のダミーデータ | 直してよい |
| `work/` | 業務画面。`nav.py`（システム名・メニュー）、`<業務>.py`（計算）、`views_<業務>.py`（画面）、`templates/work/`、`static/work/app.css` | ここを作っていく |
| `work/sample.py`・`views_sample.py`・`templates/work/sample_*.html`・`management/commands/seed_sample.py` | 業務画面の手本（サンプルの定義書のときだけ動く） | 自分の画面ができたら消す |
| `tools/` | 生成・作り直し・確かめの道具 | 直してよい |
