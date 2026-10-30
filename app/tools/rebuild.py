"""データ定義書からアプリを作り直す：モデルの生成 → DB の作り直し → ダミーデータ。
python tools/rebuild.py [定義書.xlsx]   （データベース app.db は消して作り直す）

業務のダミーデータのコマンド（seed_<業務>）を作ったら、下の SEEDS に足す。"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ["seed --reset", "seed_sample"]   # seed_sample は手本。自分の定義書では何もしない
env = dict(os.environ, PYTHONIOENCODING="utf-8", DJANGO_SUPERUSER_PASSWORD="admin")


def run(*args):
    print("$", " ".join(args), flush=True)
    subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)


run("tools/gen_models.py", *sys.argv[1:])
(ROOT / "app.db").unlink(missing_ok=True)
for a in json.loads((ROOT / "core" / "apps.json").read_text(encoding="utf-8")) + ["work"]:
    for f in (ROOT / a / "migrations").glob("0*.py"):
        f.unlink()
run("manage.py", "makemigrations", *json.loads((ROOT / "core" / "apps.json").read_text(encoding="utf-8")), "-v", "0")
run("manage.py", "migrate", "-v", "0")
run("manage.py", "createsuperuser", "--noinput", "--username", "admin", "--email", "admin@example.com")
for s in SEEDS:
    run("manage.py", *s.split())
