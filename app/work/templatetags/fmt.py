"""テンプレートの書式。{% load fmt %} で使う。"""
import os

from django import template

register = template.Library()


@register.filter
def mil(v):
    """金額を百万円・小数2桁にする：1234567 → 1.23"""
    try:
        return f"{float(v) / 1e6:,.2f}"
    except (TypeError, ValueError):
        return v


@register.filter
def num(v, digits=1):
    """数値を桁区切り・小数 digits 桁にする。空は「―」"""
    if v is None or v == "":
        return "―"
    try:
        return f"{float(v):,.{int(digits)}f}"
    except (TypeError, ValueError):
        return v


@register.simple_tag
def vstatic(path):
    """静的ファイルの URL に更新日時を付ける（CSS・JS を変えたらブラウザが必ず読み直す）。"""
    from django.contrib.staticfiles import finders
    from django.templatetags.static import static
    f = finders.find(path)
    return f"{static(path)}?v={int(os.path.getmtime(f)) if f else 0}"
