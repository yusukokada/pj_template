# 自動生成（tools/gen_models.py）。直接編集しない。
from django.contrib import admin

from core.admin_base import GeneratedAdmin
from .models import *  # noqa


@admin.register(TM1)
class TM1Admin(GeneratedAdmin):
    list_display = ['組織ID', '組織名', '上位組織ID', '有効フラグ']
    search_fields = ['組織ID', '組織名']
    list_filter = ['有効フラグ']
    derived = False


@admin.register(TM2)
class TM2Admin(GeneratedAdmin):
    list_display = ['担当者ID', '氏名', '所属組織ID', '担当者の区分', '標準単価']
    search_fields = ['担当者ID', '氏名']
    list_filter = ['担当者の区分']
    derived = False

