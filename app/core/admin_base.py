from django.contrib import admin


class GeneratedAdmin(admin.ModelAdmin):
    """生成したすべてのテーブルに共通の管理画面の設定。"""
    derived = False  # 導出テーブルは計算で作るため、画面からは編集させない
    list_per_page = 50
    show_full_result_count = True

    def get_list_select_related(self, request):
        return [f.name for f in self.model._meta.fields if f.is_relation and f.name in self.list_display]

    def has_add_permission(self, request):
        return not self.derived and super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return not self.derived and super().has_change_permission(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # 参照先の件数が多くてもプルダウンが重くならないよう、IDの直接入力＋検索窓にする
        self.raw_id_fields = tuple(f.name for f in self.model._meta.fields if f.is_relation)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
