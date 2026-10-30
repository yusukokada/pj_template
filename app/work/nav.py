"""画面の名前と左のメニュー。業務画面を足したら NAV に1行足す。"""
SYSTEM_NAME = "（システム名）"

# (グループ, 表示名, URL の名前)。グループが同じものはまとめて表示する
NAV = [
    ("全体", "ホーム", "home"),
    ("案件管理（手本）", "案件の状況", "sample_projects"),   # 手本。自分の画面に置き換えたら消す
]


def context(request):
    from django.urls import NoReverseMatch, reverse
    items = []
    for group, label, name in NAV:
        try:
            items.append((group, label, reverse(name), name))
        except NoReverseMatch:
            continue
    return {"SYSTEM_NAME": SYSTEM_NAME, "NAV": items}
