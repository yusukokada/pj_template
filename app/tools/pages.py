"""確かめる画面の一覧（smoke.py・audit_wording.py が使う）。"""
import os
import sys

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup():
    os.chdir(APP)
    sys.path.insert(0, APP)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import logging
    import django
    django.setup()
    logging.getLogger("django.request").setLevel(logging.CRITICAL)   # 開けなかった画面は smoke.py が数えて出す
    from django.conf import settings
    settings.ALLOWED_HOSTS = ["*"]
    from django.contrib.auth.models import User
    from django.test import Client
    c = Client()
    c.force_login(User.objects.get(username="admin"))
    return c


def work_urls():
    """業務画面の URL：引数のない画面すべてと、work/urls.py の SMOKE_URLS が返すもの。"""
    from work import urls as wu
    out = []
    for p in wu.urlpatterns:
        if not p.pattern.converters:
            out.append("/" + str(p.pattern))
    for fn in wu.SMOKE_URLS:
        out += fn()
    return sorted(set(out))
