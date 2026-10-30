"""業務画面。テーブル単位の画面は /admin/（マスタ・データの管理）に任せ、ここには業務の単位の画面を置く。"""
import json
from pathlib import Path

from django.apps import apps
from django.shortcuts import render

CORE = Path(__file__).resolve().parents[1] / "core"


def schema():
    p = CORE / "schema.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def home(request):
    """ホーム：領域ごとのテーブルと件数。業務画面ができるまでの入口。"""
    groups = {}
    for tid, m in schema().items():
        M = apps.get_model(m["app"], m["model"])
        groups.setdefault(m["area"], []).append(dict(
            id=tid, name=m["name"], layer=m["layer"], count=M.objects.count(),
            url=f"/admin/{m['app']}/{m['model'].lower()}/"))
    src = (CORE / "source.txt").read_text(encoding="utf-8").strip() if (CORE / "source.txt").exists() else ""
    return render(request, "work/home.html", {"nav": "home", "groups": groups, "source": src})
