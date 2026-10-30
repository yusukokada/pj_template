# 自動生成（tools/gen_models.py）。直接編集しない。
from django.apps import AppConfig


class Config(AppConfig):
    name = 'metric'
    verbose_name = '09 指標（計算で作る）'
    default_auto_field = 'django.db.models.BigAutoField'
