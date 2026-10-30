"""全画面が開けるかを確かめる：業務画面と、全テーブルの管理画面（一覧・検索・追加・詳細）。
python tools/smoke.py   （1つでも開けなければ終了コード 1）"""
import json

from pages import setup, work_urls

c = setup()
from django.apps import apps  # noqa: E402

S = json.load(open("core/schema.json", encoding="utf-8"))
bad, n = [], 0
for url in work_urls() + ["/admin/"]:
    n += 1
    r = c.get(url)
    if r.status_code != 200:
        bad.append((url, r.status_code))
for tid, m in S.items():
    M = apps.get_model(m["app"], m["model"])
    base = f"/admin/{m['app']}/{m['model'].lower()}/"
    for url in (base, base + "?q=1", base + "add/"):
        n += 1
        r = c.get(url)
        if not (r.status_code == 200 or (url.endswith("add/") and m["layer"] == "導出" and r.status_code == 403)):
            bad.append((url, r.status_code))
    o = M.objects.first()
    if o:
        n += 1
        r = c.get(base + f"{o.pk}/change/")
        if r.status_code != 200:
            bad.append((base + f"{o.pk}/change/", r.status_code))
print(f"{len(S)} テーブル・{n} 画面を開いた。開けなかった画面：{bad or 'なし'}")
raise SystemExit(1 if bad else 0)
