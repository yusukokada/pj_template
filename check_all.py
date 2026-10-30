"""ひな型（またはそこから作ったプロジェクト）が正しく動くかを、まとめて確かめる。
python check_all.py            （資料の環境・定義書の点検・アプリの作り直し・全画面・画面の文言）
python check_all.py --no-office（Excel・PowerPoint を使う確認を飛ばす）

AI が変更を終えたら、必ずこれを流して全部 OK にしてから報告する。"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
env = dict(os.environ, PYTHONIOENCODING="utf-8")
results = []


def run(name, args, cwd=ROOT, must=True):
    print(f"\n=== {name}", flush=True)
    r = subprocess.run([sys.executable, *args], cwd=cwd, env=env)
    ok = r.returncode == 0
    results.append(("OK " if ok else ("NG " if must else "注意")) + f" {name}")
    return ok


defs = [p for p in (ROOT / "docs").glob("【データ定義書】*.xlsx") if not p.name.startswith("~$")]
if len(defs) != 1:
    results.append(f"NG  docs/ の【データ定義書】が {len(defs)} 件（1つだけ置く）")
else:
    if run("データ定義書の点検", ["doc_tools/definition.py", "check", str(defs[0])]):
        if run("アプリの作り直し（生成・DB・ダミーデータ）", ["tools/rebuild.py"], cwd=ROOT / "app"):
            run("全画面が開くか", ["tools/smoke.py"], cwd=ROOT / "app")
            run("画面の文言（見つかったものは文脈で判断）", ["tools/audit_wording.py"], cwd=ROOT / "app", must=False)
if "--no-office" not in sys.argv:
    run("資料を作る環境（Excel・PowerPoint）", ["doc_tools/check_env.py"])

print("\n=== 結果")
print("\n".join(results))
sys.exit(1 if any(r.startswith("NG") for r in results) else 0)
