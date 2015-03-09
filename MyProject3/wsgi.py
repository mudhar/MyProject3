import os
import sys

sys.path.append('C:/xampp/htdocs/MyProject3/MyProject3')
sys.path.append('C:/xampp/htdocs/MyProject3')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyProject3.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
