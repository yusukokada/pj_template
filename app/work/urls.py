from django.urls import path

from . import views
from .views import schema

urlpatterns = [
    path("", views.home, name="home"),
]

# 引数つきの画面は、tools/smoke.py が開く URL を SMOKE_URLS に返す関数で足す
SMOKE_URLS = []

# 業務画面の手本。サンプルの定義書（P1〜P3）のときだけ出る
if {"P1", "P2", "P3"} <= set(schema()):
    from . import views_sample
    urlpatterns += [
        path("sample/projects/", views_sample.projects, name="sample_projects"),
        path("sample/projects/<str:pk>/", views_sample.project, name="sample_project"),
    ]
    SMOKE_URLS.append(views_sample.smoke_urls)
