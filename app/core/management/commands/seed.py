"""ダミーデータを入れる。python manage.py seed [--reset]

core/schema.json（データ定義書から生成）だけを見て、どの定義書でも動くように作ってある。値はすべて架空。
参照（FK）は、参照先に先に入れた行から選ぶ。業務画面の確認に、意味の通るデータが要るときは、
このコマンドとは別に seed_<業務> のコマンドを work/management/commands/ に作る。"""
import json
import random
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

CORE = Path(__file__).resolve().parents[2]
COUNT = {"マスタ": 12, "記録": 60, "導出": 30}   # 層ごとの件数
SURNAMES = ["佐藤", "鈴木", "高橋", "田中", "伊藤", "渡辺", "山本", "中村", "小林", "加藤", "吉田", "山田"]
GIVEN = ["一郎", "花子", "健", "美咲", "翔", "陽子", "大輔", "愛", "誠", "由美"]
START, END = date(2026, 4, 1), date(2027, 3, 31)
TZ = ZoneInfo("Asia/Tokyo")


def rdate():
    return START + timedelta(days=random.randint(0, (END - START).days))


class Command(BaseCommand):
    help = "ダミーデータを入れる"

    def add_arguments(self, p):
        p.add_argument("--reset", action="store_true", help="入れる前に全テーブルを空にする")
        p.add_argument("--seed", type=int, default=42)

    def handle(self, *args, reset=False, seed=42, **kw):
        random.seed(seed)
        self.S = json.loads((CORE / "schema.json").read_text(encoding="utf-8"))
        models = {tid: apps.get_model(m["app"], m["model"]) for tid, m in self.S.items()}
        order = self.order()
        with transaction.atomic():
            if reset:
                for tid in reversed(order):
                    models[tid].objects.all().delete()
            for tid in order:
                n = self.fill(tid, models[tid], models)
                self.stdout.write(f"{tid:5} {self.S[tid]['name']:<20} {n:>4}件")
            self.backfill(models)

    def order(self):
        """必須の参照先が先に来る順に並べる（任意の参照は後で埋める）。"""
        deps = {tid: {f["ref"] for f in m["fields"] if f["ref"] and (f["required"] or "PK" in f["key"]) and f["ref"] != tid}
                for tid, m in self.S.items()}
        done, out = set(), []
        while len(out) < len(deps):
            ready = [t for t in deps if t not in done and deps[t] <= done]
            if not ready:
                raise SystemExit(f"必須の参照が循環している：{sorted(set(deps) - done)}")
            for t in sorted(ready):
                done.add(t)
                out.append(t)
        return out

    def value(self, tid, f, i, models):
        k, name = f["kind"], f["name"]
        if k == "fk":
            rows = list(models[f["ref"]].objects.values_list("pk", flat=True)[:500])
            return models[f["ref"]].objects.get(pk=random.choice(rows)) if rows else None
        if k == "str":
            if "PK" in f["key"]:
                return f"{tid}-{i:04d}"
            if name in ("氏名", "担当者名", "名前"):
                return random.choice(SURNAMES) + " " + random.choice(GIVEN)
            if f["type"] == "文字" and "名" in name:
                return f"{self.S[tid]['name']}{i}"
            return f"{name}{i}" if f["type"] != "コード" else f"C{random.randint(1, 9)}"
        if k == "choice":
            ch = models[tid]._meta.get_field(f["field"]).choices or []
            return random.choice(ch)[0] if ch else None
        if k == "cat":
            return random.choice(["区分A", "区分B", "区分C"])
        if k == "ym":
            d = rdate()
            return f"{d.year}-{d.month:02d}"
        if k == "num":
            if "工数" in name:
                return round(random.uniform(0.5, 20), 1)
            if "数" in name:
                return random.randint(0, 30)
            return round(random.uniform(1, 100), 1)
        if k == "ratio":
            return round(random.random(), 2)
        if k == "money":
            return random.randint(10, 50000) * 1000
        if k == "date":
            return rdate()
        if k == "dt":
            d = rdate()
            return datetime(d.year, d.month, d.day, random.randint(8, 20), random.randint(0, 59), tzinfo=TZ)
        if k == "bool":
            return random.random() < 0.2
        return None

    def fill(self, tid, model, models):
        meta = self.S[tid]
        n = COUNT.get(meta["layer"], 20)
        made, tries = 0, 0
        while made < n and tries < n * 5:
            tries += 1
            kw = {}
            for f in meta["fields"]:
                v = self.value(tid, f, made + 1, models)
                if v is None and f["kind"] == "fk" and (f["required"] or "PK" in f["key"]):
                    return made   # 参照先が空のため作れない
                kw[f["field"]] = v
            self.fix_dates(kw)
            try:
                with transaction.atomic():
                    model.objects.create(**kw)
                made += 1
            except IntegrityError:
                continue   # 複合キーの重複。引き直す
        return made

    @staticmethod
    def fix_dates(kw):
        """「〜開始〜日」と「〜終了〜日」の組で、終了が開始より前なら入れ替える。"""
        for k in list(kw):
            if "開始" in k:
                e = k.replace("開始", "終了")
                if e in kw and kw[k] and kw[e] and kw[e] < kw[k]:
                    kw[k], kw[e] = kw[e], kw[k]

    def backfill(self, models):
        """先に作ったため空になった任意の参照を埋める。"""
        for tid, meta in self.S.items():
            fks = [f for f in meta["fields"] if f["kind"] == "fk" and not f["required"] and "PK" not in f["key"]]
            for obj in models[tid].objects.all() if fks else []:
                changed = False
                for f in fks:
                    if getattr(obj, f["field"] + "_id") is None and random.random() < 0.8:
                        v = self.value(tid, f, 0, models)
                        if v is not None and v.pk != obj.pk:
                            setattr(obj, f["field"], v)
                            changed = True
                if changed:
                    obj.save()
