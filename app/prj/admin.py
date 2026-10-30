# 自動生成（tools/gen_models.py）。直接編集しない。
from django.contrib import admin

from core.admin_base import GeneratedAdmin
from .models import *  # noqa


@admin.register(TP1)
class TP1Admin(GeneratedAdmin):
    list_display = ['案件ID', '案件名', '主管組織ID', '責任者ID', '案件の状態', '開始予定日', '終了予定日']
    search_fields = ['案件ID', '案件名']
    list_filter = ['案件の状態']
    derived = False


@admin.register(TP2)
class TP2Admin(GeneratedAdmin):
    list_display = ['タスクID', '案件ID', 'タスク名', '担当者ID', 'タスクの状態', '開始予定日', '終了予定日']
    search_fields = ['タスクID', 'タスク名']
    list_filter = ['タスクの状態']
    derived = False


@admin.register(TP3)
class TP3Admin(GeneratedAdmin):
    list_display = ['タスクID', '作業日', '担当者ID', '実績工数']
    search_fields = []
    list_filter = []
    derived = False

