"""業務画面の手本の画面（sample.py の計算を表示する）。"""
from django.shortcuts import render

from . import sample


def projects(request):
    rows = sample.project_status()
    warn = [r for r in rows if r["judge"] == "注意"]
    return render(request, "work/sample_projects.html", {"nav": "sample_projects", "rows": rows, "warn": warn})


def project(request, pk):
    p, rows = sample.project_detail(pk)
    return render(request, "work/sample_project.html", {"nav": "sample_projects", "p": p, "rows": rows})


def smoke_urls():
    """tools/smoke.py が開いて確かめる、引数つきの URL。"""
    first = sample.models()[0].objects.order_by("pk").first()
    return [f"/sample/projects/{first.pk}/"] if first else []
