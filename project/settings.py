
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-cn%u@7m&p*l7+s__7&&-*014+ox_=^@(+fk3$)b^-pnulo#v1$"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
import os

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'import_export',
    'corsheaders',
    'accounts',
    'banner_and_posters',
    'call_expert',
    'product',
    'contact_us',
    'home',
    'pricing',
    'dragon',
    'senior_dragon',
    'senior_unicorn',
    'unicorn', 
    'paypal.standard.ipn', 
    'shipping',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",  # Your frontend origin
    "http://localhost:8000",  # Another variant of the origin
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000", # Adjust this to your actual frontend origin
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
     'http://localhost:8000',
]


ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR,'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# database mysql using database name ikdb , username root , password root
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'ikeprinting',
#         'USER': 'root',
#         'PASSWORD': 'Er3OrDyZKh4tntWVUpwh',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# jazzmin settings

JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "IKE Printing Dashboard",
    # Title on the brand, and the login screen (19 chars max)
    "site_header": "IKE Printing Dashboard",
    "site_brand": "IKE Printing Dashboard",
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # CSS classes that are applied to the logo above
    "site_logo_bg": "",
    # Text to put in the footer of the admin site
    "site_footer": "IKE Printing Dashboard",
    # Hide the name of the dashboard site
    "site_title_hide": False,
    # Hide the URL of the dashboard site
    "site_url_hide": False,
    # show sidebar
    "navigation_expanded": True,
    # show sidebar
    "navigation_collapsed": False,
    # show sidebar
    "navigation_fixed": True,
    # show sidebar
    "navigation_reorder": False,
    
    #show view site
    "show_view_site_url": True,
    #topmenu_links 
    "topmenu_links": [
        {"name": "IKE Printing website",  "url": "http://127.0.0.1:8000/", "new_window": True},
    ],
    "copyright": "IKE Printing", 
    "navigation_expanded": True,
    #option to change theme color
    "theme": "default",
    "theme_css": "",
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    #sidebar menu icon for product app
    "icons": {
        "product.Products": "fas fa-tshirt",
    },

}

PAYPAL_RECEIVER = 'info@ikeprint.com'
PAYPAL_TEST=False

#500MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000


#zoom api key
ZOOM_ACCOUNT_ID = 'U5ZZn5XxSueETFKBY70DZw'
ZOOM_API_KEY = 'CI2GRWVlTHOC5MAqmj0QDg'
ZOOM_API_SECRET = 'HfXLfCL4vbYRwq5Tq962MoZg3KoAS0ij'


#email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'furydigitalprinting@gmail.com'
EMAIL_HOST_PASSWORD = 'wpguepqckccxvcqs'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

