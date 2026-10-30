# 自動生成（tools/gen_models.py）。直接編集しない。
from django.db import models


class TM1(models.Model):
    """M1 組織｜1行＝組織1つ｜正とする所：人事システム"""
    組織ID = models.CharField(max_length=50, primary_key=True, verbose_name='組織ID', db_column='組織ID', help_text='人事システムの組織コード')
    組織名 = models.CharField(max_length=500, verbose_name='組織名', db_column='組織名')
    上位組織ID = models.ForeignKey('master.TM1', on_delete=models.PROTECT, related_name='M1_上位組織ID', null=True, blank=True, verbose_name='上位組織ID', db_column='上位組織ID', help_text='最上位の組織は空')
    有効フラグ = models.BooleanField(default=False, verbose_name='有効フラグ', db_column='有効フラグ', help_text='廃止した組織は外す（行は消さない）')

    class Meta:
        db_table = 'm1'
        verbose_name = verbose_name_plural = 'M1 組織'

    def __str__(self):
        return f"{self.組織ID} {self.組織名}"


class TM2(models.Model):
    """M2 担当者｜1行＝担当者1人｜正とする所：人事システム（委託先は契約台帳）"""
    担当者ID = models.CharField(max_length=50, primary_key=True, verbose_name='担当者ID', db_column='担当者ID')
    氏名 = models.CharField(max_length=500, verbose_name='氏名', db_column='氏名')
    所属組織ID = models.ForeignKey('master.TM1', on_delete=models.PROTECT, related_name='M2_所属組織ID', verbose_name='所属組織ID', db_column='所属組織ID')
    担当者の区分 = models.CharField(max_length=50, choices=[('EMP', '社員'), ('VND', '委託先')], verbose_name='担当者の区分', db_column='担当者の区分')
    標準単価 = models.BigIntegerField(null=True, blank=True, verbose_name='標準単価', db_column='標準単価', help_text='1人日あたりの円')

    class Meta:
        db_table = 'm2'
        verbose_name = verbose_name_plural = 'M2 担当者'

    def __str__(self):
        return f"{self.担当者ID} {self.氏名}"

