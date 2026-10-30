import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 手元の試作用。本番に出すときは SECRET_KEY・DEBUG・ALLOWED_HOSTS を必ず変える
SECRET_KEY = "local-prototype-only"
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 領域ごとのアプリは tools/gen_models.py がデータ定義書から作り、名前を core/apps.json に書く
_apps = BASE_DIR / "core" / "apps.json"
DOMAIN_APPS = json.loads(_apps.read_text(encoding="utf-8")) if _apps.exists() else []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "core",
    "work.apps.Config",
] + [f"{a}.apps.Config" for a in DOMAIN_APPS]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "work.nav.context",
    ]},
}]

# PostgreSQL に移すときは、ここを ENGINE=django.db.backends.postgresql と接続先に書き換える
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "app.db"}}

LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000
