"""業務画面の手本（サンプルの定義書の P1 案件・P2 タスク・P3 工数実績を使う）。

自分のプロジェクトの定義書に置き換えたら、このファイル・views_sample.py・templates/work/sample_*.html を消し、
同じ形（計算はこのような関数に分け、画面は views に置く）で業務の画面を作る。

判断を求める画面には、問い・診断・原因・推奨を置く（rules/screen-design.md）。"""
from datetime import date, timedelta

from django.apps import apps
from django.db.models import Sum

# 判定の境界。本来は定義書の指標の定義（マスタ）から読む。コードに直書きするのは手本だから
LATE_WARN = 1      # 遅延タスクがこの数以上で「注意」
EFFORT_WARN = 1.2  # 実績工数が計画工数のこの倍以上で「注意」


def models():
    get = apps.get_model
    return get("prj", "TP1"), get("prj", "TP2"), get("prj", "TP3")


def project_status(today=None):
    """案件ごとの進捗と判定。"""
    today = today or date.today()
    P1, P2, P3 = models()
    out = []
    for p in P1.objects.select_related("責任者ID").order_by("案件ID"):
        tasks = P2.objects.filter(案件ID=p)
        done = tasks.filter(タスクの状態="DONE").count()
        late = tasks.exclude(タスクの状態="DONE").filter(終了予定日__lt=today).count()
        plan = tasks.aggregate(s=Sum("計画工数"))["s"] or 0
        actual = P3.objects.filter(タスクID__案件ID=p).aggregate(s=Sum("実績工数"))["s"] or 0
        # 工数の超過は、終わったタスクどうしで比べる（途中のタスクを入れると、実績が少なく見える）
        dplan = tasks.filter(タスクの状態="DONE").aggregate(s=Sum("計画工数"))["s"] or 0
        dact = P3.objects.filter(タスクID__案件ID=p, タスクID__タスクの状態="DONE").aggregate(s=Sum("実績工数"))["s"] or 0
        ratio = dact / dplan if dplan else None
        reasons = []
        if late >= LATE_WARN:
            reasons.append(f"終了予定日を過ぎた未完了のタスク {late} 件")
        if ratio is not None and ratio >= EFFORT_WARN:
            reasons.append(f"完了タスクの実績工数が計画工数の {ratio:.2f} 倍")
        out.append(dict(
            id=p.pk, name=p.案件名, owner=str(p.責任者ID.氏名), state=p.get_案件の状態_display(),
            tasks=tasks.count(), done=done, late=late, plan=round(plan, 1), actual=round(actual, 1), ratio=ratio,
            judge="注意" if reasons else "良好", reasons=reasons))
    return out


def build_weekly(today=None, weeks=8):
    """D1 案件の週次進捗（導出）を、P1〜P3 から計算して作り直す。導出のテーブルは人が入力せず、このような関数で作る。"""
    today = today or date.today()
    P1, P2, P3 = models()
    D1 = apps.get_model("metric", "TD1")
    D1.objects.all().delete()
    friday = today - timedelta(days=(today.weekday() - 4) % 7)
    n = 0
    for p in P1.objects.all():
        tasks = P2.objects.filter(案件ID=p)
        for w in range(weeks):
            d = friday - timedelta(weeks=w)
            D1.objects.create(
                案件ID=p, 基準日=d,
                計画工数=tasks.filter(終了予定日__lte=d).aggregate(s=Sum("計画工数"))["s"] or 0,
                実績工数=P3.objects.filter(タスクID__案件ID=p, 作業日__lte=d).aggregate(s=Sum("実績工数"))["s"] or 0,
                完了タスク数=tasks.filter(完了日__lte=d).count(),
                遅延タスク数=tasks.filter(終了予定日__lt=d).exclude(完了日__lte=d).count())
            n += 1
    return n


def project_detail(pk, today=None):
    today = today or date.today()
    P1, P2, P3 = models()
    p = P1.objects.get(pk=pk)
    rows = []
    for t in P2.objects.filter(案件ID=p).select_related("担当者ID").order_by("終了予定日"):
        actual = P3.objects.filter(タスクID=t).aggregate(s=Sum("実績工数"))["s"] or 0
        rows.append(dict(id=t.pk, name=t.タスク名, who=t.担当者ID.氏名 if t.担当者ID else "―",
                         state=t.get_タスクの状態_display(), end=t.終了予定日, plan=t.計画工数, actual=round(actual, 1),
                         late=t.タスクの状態 != "DONE" and t.終了予定日 < today))
    return p, rows
