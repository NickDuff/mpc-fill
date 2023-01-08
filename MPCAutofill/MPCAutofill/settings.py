"""
Django settings for MPCAutofill project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import django_stubs_ext
import environ

django_stubs_ext.monkeypatch()  # https://stackoverflow.com/q/67965529

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Production-specific settings kept in .env, modify the .env.dist then rename
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
env.read_env(os.path.join(BASE_DIR, "MPCAutofill/.env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", default="-")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG", default=False)

# IP or Domain
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# Unique site information
GTAG = env("GTAG", default="")  # Google Analytics
SITE_NAME = env("SITE_NAME", default="MPC Autofill")
TARGET_EMAIL = env("TARGET_EMAIL", default="your_email@somewhere.com")
DISCORD = env("DISCORD", default="http://mprox.link/discord")
REDDIT = env("REDDIT", default="https://www.reddit.com/r/mpcproxies/")
THEME = env("THEME", default="superhero")

PREPEND_WWW = env("PREPEND_WWW", default=False)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]  # required for Docker with Django 4.x+

# Application definition

INSTALLED_APPS = [
    "cardpicker.apps.CardpickerConfig",
    "blog.apps.BlogConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_elasticsearch_dsl",
    "crispy_forms",
    "django_user_agents",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
]

ROOT_URLCONF = "MPCAutofill.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cardpicker.context_processors.add_site_info",
                "cardpicker.context_processors.common_info",
            ],
        },
    },
]

WSGI_APPLICATION = "MPCAutofill.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": env("DATABASE_NAME", default=os.path.join(BASE_DIR, "card_db.db")),
        "USER": env("DATABASE_USER", default="mpcautofill"),
        "PASSWORD": env("DATABASE_PASSWORD", default="mpcautofill"),
        "HOST": env("DATABASE_HOST", default="postgres"),
        "PORT": env("DATABASE_PORT", default=5432),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = env("LANG_CODE", default="en-us")

TIME_ZONE = env("TIME_ZONE", default="America/New_York")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/" + env("STATIC", default="static") + "/"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATICFILES_DIRS = [
    os.path.normpath(os.path.join(BASE_DIR, "cardpicker/static")),
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), env("STATIC", default="static"))

# elasticsearch DSL settings
ELASTICSEARCH_HOST = env("ELASTICSEARCH_HOST", default="localhost")
ELASTICSEARCH_DSL = {
    "default": {"hosts": f"{ELASTICSEARCH_HOST}:9200"},
}

ELASTICSEARCH_DSL_AUTOSYNC = False

# Email for logging
ADMINS = [("admin", env("TARGET_EMAIL", default=""))]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = env("DJANGO_GMAIL", default="")
EMAIL_HOST_PASSWORD = env("DJANGO_GMAIL_PASSWORD", default="")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "default from email"

# Database update settings
DEFAULT_CARDBACK_FOLDER_PATH = env("DEFAULT_CARDBACK_FOLDER_PATH", default="Chilli_Axe's MTG Renders / 12. Cardbacks")
DEFAULT_CARDBACK_IMAGE_NAME = env("DEFAULT_CARDBACK_IMAGE_NAME", default="Black Lotus")

# PATREON
PATREON_ENABLED = env("PATREON_ENABLED", default=False)
PATREON_URL = env("PATREON_URL", default="http://patreon.com/mpcfill")
PATREON_KEY = env("PATREON_KEY", default="")
