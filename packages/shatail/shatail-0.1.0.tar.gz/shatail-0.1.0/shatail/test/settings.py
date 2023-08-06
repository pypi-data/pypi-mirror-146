import os

from django.contrib.messages import constants as message_constants
from django.utils.translation import gettext_lazy as _

DEBUG = False
SHATAIL_ROOT = os.path.dirname(os.path.dirname(__file__))
SHATAILADMIN_BASE_URL = "http://testserver"
STATIC_ROOT = os.path.join(SHATAIL_ROOT, "tests", "test-static")
MEDIA_ROOT = os.path.join(SHATAIL_ROOT, "tests", "test-media")
MEDIA_URL = "/media/"

TIME_ZONE = "Asia/Tokyo"

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DATABASE_NAME", ":memory:"),
        "USER": os.environ.get("DATABASE_USER", ""),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", ""),
        "HOST": os.environ.get("DATABASE_HOST", ""),
        "PORT": os.environ.get("DATABASE_PORT", ""),
        "TEST": {"NAME": os.environ.get("DATABASE_NAME", "")},
    }
}

# Set regular database name when a non-SQLite db is used
if DATABASES["default"]["ENGINE"] != "django.db.backends.sqlite3":
    DATABASES["default"]["NAME"] = os.environ.get("DATABASE_NAME", "shatail")

# Add extra options when mssql is used (on for example appveyor)
if DATABASES["default"]["ENGINE"] == "sql_server.pyodbc":
    DATABASES["default"]["OPTIONS"] = {
        "driver": os.environ.get("DATABASE_DRIVER", "SQL Server Native Client 11.0"),
        "MARS_Connection": "True",
        "host_is_server": True,  # Applies to FreeTDS driver only
    }


# explicitly set charset / collation to utf8 on mysql
if DATABASES["default"]["ENGINE"] == "django.db.backends.mysql":
    DATABASES["default"]["TEST"]["CHARSET"] = "utf8"
    DATABASES["default"]["TEST"]["COLLATION"] = "utf8_general_ci"


SECRET_KEY = "not needed"

ROOT_URLCONF = "shatail.test.urls"

STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

USE_TZ = not os.environ.get("DISABLE_TIMEZONE")
if not USE_TZ:
    print("Timezone support disabled")

LANGUAGE_CODE = "en"

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
                "django.template.context_processors.request",
                "shatail.test.context_processors.do_not_use_static_url",
                "shatail.contrib.settings.context_processors.settings",
            ],
            "debug": True,  # required in order to catch template errors
        },
    },
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "APP_DIRS": False,
        "DIRS": [
            os.path.join(SHATAIL_ROOT, "test", "testapp", "jinja2_templates"),
        ],
        "OPTIONS": {
            "extensions": [
                "shatail.jinja2tags.core",
                "shatail.admin.jinja2tags.userbar",
                "shatail.images.jinja2tags.images",
                "shatail.contrib.settings.jinja2tags.settings",
            ],
        },
    },
]

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "shatail.test.middleware.BlockDodgyUserAgentMiddleware",
    "shatail.contrib.redirects.middleware.RedirectMiddleware",
)

INSTALLED_APPS = [
    # Install shatailredirects with its appconfig
    # There's nothing special about shatailredirects, we just need to have one
    # app which uses AppConfigs to test that hooks load properly
    "shatail.contrib.redirects.apps.ShatailRedirectsAppConfig",
    "shatail.test.testapp",
    "shatail.test.demosite",
    "shatail.test.snippets",
    "shatail.test.routablepage",
    "shatail.test.search",
    "shatail.test.modeladmintest",
    "shatail.test.i18n",
    "shatail.contrib.simple_translation",
    "shatail.contrib.styleguide",
    "shatail.contrib.routable_page",
    "shatail.contrib.frontend_cache",
    "shatail.contrib.search_promotions",
    "shatail.contrib.settings",
    "shatail.contrib.modeladmin",
    "shatail.contrib.table_block",
    "shatail.contrib.forms",
    "shatail.contrib.typed_table_block",
    "shatail.search",
    "shatail.embeds",
    "shatail.images",
    "shatail.sites",
    "shatail.locales",
    "shatail.users",
    "shatail.snippets",
    "shatail.documents",
    "shatail.admin",
    "shatail.api.v2",
    "shatail",
    "taggit",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
]


# Using DatabaseCache to make sure that the cache is cleared between tests.
# This prevents false-positives in some shatail core tests where we are
# changing the 'shatail_root_paths' key which may cause future tests to fail.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",
    }
}

PASSWORD_HASHERS = (
    "django.contrib.auth.hashers.MD5PasswordHasher",  # don't use the intentionally slow default password hasher
)

ALLOWED_HOSTS = ["localhost", "testserver", "other.example.com"]

SHATAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "shatail.search.backends.database.fallback",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if os.environ.get("USE_EMAIL_USER_MODEL"):
    INSTALLED_APPS.append("shatail.test.emailuser")
    AUTH_USER_MODEL = "emailuser.EmailUser"
    print("EmailUser (no username) user model active")
else:
    INSTALLED_APPS.append("shatail.test.customuser")
    AUTH_USER_MODEL = "customuser.CustomUser"
    # Extra user field for custom user edit and create form tests. This setting
    # needs to here because it is used at the module level of shatailusers.forms
    # when the module gets loaded. The decorator 'override_settings' does not work
    # in this scenario.
    SHATAIL_USER_CUSTOM_FIELDS = ["country", "attachment"]

if os.environ.get("DATABASE_ENGINE") == "django.db.backends.postgresql":
    SHATAILSEARCH_BACKENDS["postgresql"] = {
        "BACKEND": "shatail.search.backends.database",
        "AUTO_UPDATE": False,
        "SEARCH_CONFIG": "english",
    }

if "ELASTICSEARCH_URL" in os.environ:
    if os.environ.get("ELASTICSEARCH_VERSION") == "7":
        backend = "shatail.search.backends.elasticsearch7"
    elif os.environ.get("ELASTICSEARCH_VERSION") == "6":
        backend = "shatail.search.backends.elasticsearch6"
    elif os.environ.get("ELASTICSEARCH_VERSION") == "5":
        backend = "shatail.search.backends.elasticsearch5"

    SHATAILSEARCH_BACKENDS["elasticsearch"] = {
        "BACKEND": backend,
        "URLS": [os.environ["ELASTICSEARCH_URL"]],
        "TIMEOUT": 10,
        "max_retries": 1,
        "AUTO_UPDATE": False,
        "INDEX_SETTINGS": {"settings": {"index": {"number_of_shards": 1}}},
    }


SHATAIL_SITE_NAME = "Test Site"

SHATAILADMIN_RICH_TEXT_EDITORS = {
    "default": {"WIDGET": "shatail.admin.rich_text.DraftailRichTextArea"},
    "custom": {"WIDGET": "shatail.test.testapp.rich_text.CustomRichTextArea"},
}

SHATAIL_CONTENT_LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
]


# Set a non-standard DEFAULT_AUTHENTICATION_CLASSES value, to verify that the
# admin API still works with session-based auth regardless of this setting
# (see https://github.com/shatail/shatail/issues/5585)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
    ]
}

# Disable redirect autocreation for the majority of tests (to improve efficiency)
SHATAILREDIRECTS_AUTO_CREATE = False


# https://github.com/shatail/shatail/issues/2551 - projects should be able to set
# MESSAGE_TAGS for their own purposes without them leaking into Shatail admin styles.

MESSAGE_TAGS = {
    message_constants.DEBUG: "my-custom-tag",
    message_constants.INFO: "my-custom-tag",
    message_constants.SUCCESS: "my-custom-tag",
    message_constants.WARNING: "my-custom-tag",
    message_constants.ERROR: "my-custom-tag",
}
