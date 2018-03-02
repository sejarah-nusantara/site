from django.conf import settings
from django.utils import translation


class SetAdminLanguage(object):
    def process_request(self, request):
#         if 'admin' in request.path_info:
        if request.path.startswith('/admin'):
            request.LANG = getattr(settings, 'ADMIN_LANGUAGE_CODE', settings.LANGUAGE_CODE)
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG