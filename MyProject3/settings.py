import os
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'Helpdesk/Templates')]
HELPDESK_DIRS = os.path.join(BASE_DIR, 'Helpdesk')
STATIC_ROOT = 'C:/xampp/htdocs/MyProject3/Helpdesk/Static'
STATIC_URL = '/Helpdesk/Static/'
SECRET_KEY = '%3d*yo%ut#^-xv2r7acmxi!ag&pcd@3^dz0dndo50_nq_nuzdj'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'Helpdesk.Users'
'''TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)'''
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Helpdesk',
)
MIDDLEWARE_CLASSES = (
    'firepy.django.middleware.FirePHPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'MyProject3.urls'
WSGI_APPLICATION = 'MyProject3.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django', 
        'NAME': 'myproject3',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
          'autocommit': True,
        },
    }
}
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'saradanhelpdesk@gmail.com'
EMAIL_HOST_PASSWORD = 'rizkiasus'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
