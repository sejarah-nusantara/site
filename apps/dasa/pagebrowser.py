import sys
from django.conf import settings
if settings.PATH_TO_INGBOOK_PRODUCT not in sys.path:
    sys.path.append(settings.PATH_TO_INGBOOK_PRODUCT)

from pagebrowser_api import *
