from pathlib import Path          # tool for working with folder addresses
import environ                    # tool that reads the .env file

BASE_DIR = Path(__file__).resolve().parent.parent
# __file__ is this file; .resolve() gives its full address; each .parent climbs one folder
# (settings.py -> config -> ranker-rag). So BASE_DIR is the project root.

env = environ.Env()                              # the reader of secret settings
environ.Env.read_env(BASE_DIR / ".env")          # read the .env file in the root

SECRET_KEY = env("DJANGO_SECRET_KEY")            # no default, so the app refuses to start without it
DEBUG = env.bool("DEBUG", default=False)         # read DEBUG as True/False; safe default False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
# env.list splits "a,b" into ["a", "b"]

INSTALLED_APPS = [
    "django.contrib.admin",            # the admin screen
    "django.contrib.auth",             # users and login
    "django.contrib.contenttypes",     # Django's internal bookkeeping
    "django.contrib.sessions",         # remembers logged-in users
    "django.contrib.messages",         # one-time messages
    "django.contrib.staticfiles",      # CSS/JS files for the admin
    "rest_framework",                  # the API kit we just installed
    "apps.documents",                  # our upload app (full path, from Step 1)
    "apps.chat",                       # our chat app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",            # basic security protections
    "django.contrib.sessions.middleware.SessionMiddleware",     # needed before login support
    "django.middleware.common.CommonMiddleware",                # small URL fixes
    "django.middleware.csrf.CsrfViewMiddleware",                # blocks fake form submissions
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # knows who the user is
    "django.contrib.messages.middleware.MessageMiddleware",     # message support
    "django.middleware.clickjacking.XFrameOptionsMiddleware",   # stops hidden-frame tricks
]
# Middleware = guards every request walks past, in this order.

ROOT_URLCONF = "config.urls"                      # where the address book lives

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",  # HTML page engine (used by admin)
    "DIRS": [BASE_DIR / "templates"],     # look for templates in the templates folder in the project root                                                   # no extra template folders
    "APP_DIRS": True,                                              # also look inside each app
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",              # gives pages the request
        "django.contrib.auth.context_processors.auth",             # gives pages the user
        "django.contrib.messages.context_processors.messages",     # gives pages messages
    ]},
}]

WSGI_APPLICATION = "config.wsgi.application"      # the door Gunicorn uses later in Docker

DATABASES = {"default": env.db(
    "DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
)}
# Reads a DATABASE_URL if set; otherwise uses a simple local SQLite file.
# We switch to Postgres with pgvector in Step 4.

LANGUAGE_CODE = "en-us"                           # language of Django's own text
TIME_ZONE = "UTC"                                 # store times in UTC
USE_TZ = True                                     # always use timezone-aware times

STATIC_URL = "/static/"                           # web address of static files
STATIC_ROOT = BASE_DIR / "staticfiles"            # where collected static files go for Docker
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"   # row ids are big whole numbers
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")   # trust Vercel's note that the visitor used https
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])   # extra sites allowed to post forms (empty for now)