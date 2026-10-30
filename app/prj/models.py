# 自動生成（tools/gen_models.py）。直接編集しない。
from django.db import models


class TP1(models.Model):
    """P1 案件｜1行＝案件1件｜正とする所：このシステム"""
    案件ID = models.CharField(max_length=50, primary_key=True, verbose_name='案件ID', db_column='案件ID')
    案件名 = models.CharField(max_length=500, verbose_name='案件名', db_column='案件名')
    主管組織ID = models.ForeignKey('master.TM1', on_delete=models.PROTECT, related_name='P1_主管組織ID', verbose_name='主管組織ID', db_column='主管組織ID')
    責任者ID = models.ForeignKey('master.TM2', on_delete=models.PROTECT, related_name='P1_責任者ID', verbose_name='責任者ID', db_column='責任者ID')
    案件の状態 = models.CharField(max_length=50, choices=[('PLAN', '計画中'), ('RUN', '実施中'), ('DONE', '完了'), ('STOP', '中止')], verbose_name='案件の状態', db_column='案件の状態')
    開始予定日 = models.DateField(verbose_name='開始予定日', db_column='開始予定日')
    終了予定日 = models.DateField(verbose_name='終了予定日', db_column='終了予定日')
    予算 = models.BigIntegerField(null=True, blank=True, verbose_name='予算', db_column='予算', help_text='承認された予算の総額（円）')

    class Meta:
        db_table = 'p1'
        verbose_name = verbose_name_plural = 'P1 案件'

    def __str__(self):
        return f"{self.案件ID} {self.案件名}"


class TP2(models.Model):
    """P2 タスク｜1行＝タスク1つ｜正とする所：このシステム"""
    タスクID = models.CharField(max_length=50, primary_key=True, verbose_name='タスクID', db_column='タスクID')
    案件ID = models.ForeignKey('prj.TP1', on_delete=models.PROTECT, related_name='P2_案件ID', verbose_name='案件ID', db_column='案件ID')
    タスク名 = models.CharField(max_length=500, verbose_name='タスク名', db_column='タスク名')
    担当者ID = models.ForeignKey('master.TM2', on_delete=models.PROTECT, related_name='P2_担当者ID', null=True, blank=True, verbose_name='担当者ID', db_column='担当者ID')
    タスクの状態 = models.CharField(max_length=50, choices=[('TODO', '未着手'), ('DOING', '着手'), ('DONE', '完了')], verbose_name='タスクの状態', db_column='タスクの状態')
    開始予定日 = models.DateField(verbose_name='開始予定日', db_column='開始予定日')
    終了予定日 = models.DateField(verbose_name='終了予定日', db_column='終了予定日')
    計画工数 = models.FloatField(verbose_name='計画工数', db_column='計画工数', help_text='人日')
    完了日 = models.DateField(null=True, blank=True, verbose_name='完了日', db_column='完了日', help_text='完了したときだけ入れる')

    class Meta:
        db_table = 'p2'
        verbose_name = verbose_name_plural = 'P2 タスク'

    def __str__(self):
        return f"{self.タスクID} {self.タスク名}"


class TP3(models.Model):
    """P3 工数実績｜1行＝タスク×作業日×担当者｜正とする所：このシステム"""
    タスクID = models.ForeignKey('prj.TP2', on_delete=models.PROTECT, related_name='P3_タスクID', verbose_name='タスクID', db_column='タスクID')
    作業日 = models.DateField(verbose_name='作業日', db_column='作業日')
    担当者ID = models.ForeignKey('master.TM2', on_delete=models.PROTECT, related_name='P3_担当者ID', verbose_name='担当者ID', db_column='担当者ID')
    実績工数 = models.FloatField(verbose_name='実績工数', db_column='実績工数', help_text='人日')

    class Meta:
        db_table = 'p3'
        verbose_name = verbose_name_plural = 'P3 工数実績'
        constraints = [models.UniqueConstraint(fields=['タスクID', '作業日', '担当者ID'], name='uq_p3')]

    def __str__(self):
        return f"{self.タスクID_id} / {self.作業日} / {self.担当者ID_id}"

