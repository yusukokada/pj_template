# 自動生成（tools/gen_models.py）。直接編集しない。
from django.apps import AppConfig


class Config(AppConfig):
    name = 'master'
    verbose_name = '00 共通マスタ'
    default_auto_field = 'django.db.models.BigAutoField'
