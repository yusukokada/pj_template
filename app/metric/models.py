# 自動生成（tools/gen_models.py）。直接編集しない。
from django.db import models


class TD1(models.Model):
    """D1 案件の週次進捗｜1行＝案件×基準日｜正とする所：このシステム（P1〜P3 から計算）"""
    案件ID = models.ForeignKey('prj.TP1', on_delete=models.PROTECT, related_name='D1_案件ID', verbose_name='案件ID', db_column='案件ID')
    基準日 = models.DateField(verbose_name='基準日', db_column='基準日', help_text='毎週金曜')
    計画工数 = models.FloatField(null=True, blank=True, verbose_name='計画工数', db_column='計画工数', help_text='終了予定日が基準日までのタスクの計画工数の合計')
    実績工数 = models.FloatField(null=True, blank=True, verbose_name='実績工数', db_column='実績工数', help_text='基準日までの P3 実績工数の合計')
    完了タスク数 = models.FloatField(null=True, blank=True, verbose_name='完了タスク数', db_column='完了タスク数')
    遅延タスク数 = models.FloatField(null=True, blank=True, verbose_name='遅延タスク数', db_column='遅延タスク数', help_text='終了予定日を過ぎて完了していないタスクの数')

    class Meta:
        db_table = 'd1'
        verbose_name = verbose_name_plural = 'D1 案件の週次進捗'
        constraints = [models.UniqueConstraint(fields=['案件ID', '基準日'], name='uq_d1')]

    def __str__(self):
        return f"{self.案件ID_id} / {self.基準日}"

