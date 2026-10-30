# 自動生成（tools/gen_models.py）。直接編集しない。
from django.contrib import admin

from core.admin_base import GeneratedAdmin
from .models import *  # noqa


@admin.register(TD1)
class TD1Admin(GeneratedAdmin):
    list_display = ['案件ID', '基準日', '計画工数', '実績工数', '完了タスク数', '遅延タスク数']
    search_fields = []
    list_filter = []
    derived = True

