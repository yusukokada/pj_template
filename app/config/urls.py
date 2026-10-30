from django.contrib import admin
from django.urls import include, path

from work.nav import SYSTEM_NAME

admin.site.site_header = f"{SYSTEM_NAME}｜マスタ・データの管理"
admin.site.site_title = SYSTEM_NAME
admin.site.index_title = "領域別のテーブル"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("work.urls")),
]
