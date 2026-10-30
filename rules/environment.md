# Windows・ターミナル・Python

- Python の出力に日本語を含むときは、`PYTHONIOENCODING=utf-8` を付けるか、UTF-8 のファイルに書いてから読む（Windows のターミナルは cp932 で、付けないと文字化けか例外になる）。PowerShell なら `$env:PYTHONIOENCODING = "utf-8"`
- pptx の見た目は PowerPoint（COM）で PNG にして確かめる：`python doc_tools/render_pptx.py "docs/<ファイル>.pptx" [ページ]`。出力は `doc_tools/render/`（Git に入れない）
- 画面の見た目は、`cd app` → `python manage.py runserver` で http://127.0.0.1:8000 を開く（`start.bat` でもよい）。ログインは admin／admin（手元専用）
- pip が遅くてタイムアウトする環境では `python -m pip install --timeout 300 --retries 10 -r <requirements.txt>`
- 一時的なスクリプトは `doc_tools/work/` に置く（Git に入れない）。残す価値のあるものは `doc_tools/examples/` に移し、冒頭に何をするものかを書く
