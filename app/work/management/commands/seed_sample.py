"""業務画面の手本のダミーデータ：意味の通る案件・タスク・工数実績を作り、D1 案件の週次進捗を計算する。
python manage.py seed_sample   （サンプルの定義書でないときは何もしない）

seed（どの定義書でも動く乱数のデータ）の後に流す。業務の画面を作ったら、同じ形で seed_<業務> を作る。"""
import random
from datetime import date, timedelta

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction

from work import sample
from work.views import schema

NAMES = ["基幹システム更改", "経費精算の電子化", "顧客ポータル刷新", "データ基盤構築", "認証基盤統合",
         "在庫管理の改修", "BI ダッシュボード導入", "ネットワーク更改"]
TASKS = ["要件定義", "基本設計", "詳細設計", "製造", "単体テスト", "結合テスト", "総合テスト", "移行", "受入支援", "運用設計"]


class Command(BaseCommand):
    help = "業務画面の手本のダミーデータ"

    def handle(self, *args, **kw):
        if not {"P1", "P2", "P3", "D1"} <= set(schema()):
            self.stdout.write("サンプルの定義書ではないため、何もしない")
            return
        random.seed(7)
        get = apps.get_model
        M2, P1, P2, P3, D1 = (get("master", "TM2"), get("prj", "TP1"), get("prj", "TP2"), get("prj", "TP3"), get("metric", "TD1"))
        today = date.today()
        people = list(M2.objects.all())
        with transaction.atomic():
            for M in (D1, P3, P2, P1):
                M.objects.all().delete()
            for i, name in enumerate(NAMES, 1):
                start = today - timedelta(days=random.randint(20, 120))
                owner = random.choice(people)
                p = P1.objects.create(案件ID=f"P1-{i:04d}", 案件名=name, 主管組織ID=owner.所属組織ID, 責任者ID=owner,
                                      案件の状態="RUN", 開始予定日=start, 終了予定日=start + timedelta(days=180),
                                      予算=random.randint(20, 300) * 1_000_000)
                slip = i in (2, 7)       # 遅れている案件（手本で「注意」が出るように決めておく）
                over = i in (4, 7)       # 工数が計画を超えている案件
                d = start
                for j, tname in enumerate(TASKS, 1):
                    end = d + timedelta(days=random.randint(10, 20))
                    plan = round(random.uniform(5, 25), 1)
                    if end < today and not (slip and end > today - timedelta(days=30)):
                        state, done = "DONE", end
                    elif d <= today:
                        state, done = "DOING", None
                    else:
                        state, done = "TODO", None
                    who = random.choice(people)
                    t = P2.objects.create(タスクID=f"P2-{i:02d}{j:02d}", 案件ID=p, タスク名=tname, 担当者ID=who,
                                          タスクの状態=state, 開始予定日=d, 終了予定日=end, 計画工数=plan, 完了日=done)
                    if state != "TODO":
                        rate = random.uniform(1.25, 1.5) if over else random.uniform(0.8, 1.05)
                        days = max(1, (min(end, today) - d).days // 3)
                        for k in range(days):
                            P3.objects.create(タスクID=t, 作業日=d + timedelta(days=k * 3), 担当者ID=who,
                                              実績工数=round(plan * rate / days, 2))
                    d = end + timedelta(days=1)
            n = sample.build_weekly(today)
        self.stdout.write(f"案件 {P1.objects.count()} 件・タスク {P2.objects.count()} 件・工数実績 {P3.objects.count()} 件・週次進捗 {n} 件")
