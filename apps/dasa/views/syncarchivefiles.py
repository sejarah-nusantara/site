#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013-
#


import os
import types
from datetime import datetime

from django.core.paginator import Page as PaginatorPage, Paginator, InvalidPage
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.generic.base import RedirectView
from django.core import urlresolvers
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout as Signout
from django.views.generic import TemplateView
from django.views.generic import View
from django.conf import settings

from haystack.query import SearchQuerySet
from haystack.views import SearchView

from sorl.thumbnail import get_thumbnail

from userena.decorators import secure_required
from userena.utils import get_profile_model, get_user_model
from userena.views import ExtraContextTemplateView, userena_settings
from userena.models import UserenaSignup

from guardian.decorators import permission_required

from dasa import config, models
from dasa import forms
from dasa import queries
from dasa.utils import sluggify, urlencode
from dasa.pagebrowser import PageBrowserBook
from dasa.repository import repository
from dasa.utils import get_page
from dasa import utils

from common import DasaSearchView, Page, translate, admin_link, prettyprint_query, _tagcloud
from common import repository_logger

"""
Algemeen:
=====================
Corpus Diplomaticum Neerlando-Indicum

Verzameling van Politieke contracten en verdere Verdragen door de Nederlanders in het Oosten gesloten, van Privilegebrieven, aan heb verleend, enz.


Per deel:
=====================
"""
CORPUSDIPLOMATICUMTITLES = [
    "Corpus Diplomaticum Volume 1 (1596 - 1650), Mr. J. E. Heeres, KITLV 57, 1907",
    "Corpus Diplomaticum Volume 2 (1650 - 1675), Mr. J. E. Heeres, KITLV 87, 1931",
    "Corpus Diplomaticum Volume 3 (1676 - 1691), Prof. Mr. J. E. Heeres, KITLV 91, 1934",
    "Corpus Diplomaticum Volume 4 (1691 - 1725), Dr. F. W. Stapel, KITLV 93, 1935",
    "Corpus Diplomaticum Volume 5 (1726 - 1752), Dr. F. W. Stapel, KITLV 96, 1938",
    "Corpus Diplomaticum Volume 6 (1753 - 1799), Dr. F. W. Stapel, KITLV, 1955",
]


class SyncArchiveFiles(TemplateView):
    template_name = 'admin/sync_archivefiles.html'

    def get_context_data(self):

        context = {
            'settings': settings,
            'REPOSITORY_URL': settings.REPOSITORY_URL,
            'REPOSITORY_PUBLIC_URL': settings.REPOSITORY_PUBLIC_URL,
            'PAGEBROWSER_URL': settings.PAGEBROWSER_URL,
            'PAGEBROWSER_PUBLIC_URL': settings.PAGEBROWSER_PUBLIC_URL,
            'PAGEBROWSER_ADMIN_URL': settings.PAGEBROWSER_ADMIN_URL,
            'view': self,
            # 'archivefiles_from_repo': self.published_archivefiles_from_repo,
        }

        return context

    def get(self, request, *args, **kwargs):

        msg = ''

        self.pagebrowser = PageBrowserBook(settings.PAGEBROWSER_URL, auth=settings.PAGEBROWSER_AUTH)
        now = datetime.now().isoformat()

        if 'publish' in request.GET:
            archivefile_id = self.request.GET.get('archivefile')
            ead_id = self.request.GET.get('ead_id')

            def raise_404(error):
                repository_logger.error('[2] [{0}] ERROR: {1}'.format(now, unicode(error)))
                response = HttpResponse('Error: ' + unicode(error))
                response.status_code = 404
                return response

            try:
                msg = self.publish_in_pagebrowser(ead_id=ead_id, archivefile_id=archivefile_id)
                repository_logger.info('[3] [{0}] {1}'.format(now, msg))
            except Exception as error:
                if 'ConflictError' in error:
                    # a conflict error: we try again
                    try:
                        msg = self.publish_in_pagebrowser(ead_id=ead_id, archivefile_id=archivefile_id)
                        repository_logger.info('[4] [{0}] {1}'.format(now, msg))
                    except Exception, error:
                        raise_404(error)
                else:
                    raise_404(error)

            if 'redirect' in request.GET:
                return redirect('{0}?message={1}'.format(urlresolvers.reverse('sync_archivefiles'), msg))
            else:
                return HttpResponse('Updated %s - %s [%s]' % (ead_id, archivefile_id, msg))

        elif 'delete' in request.GET:
            archivefile_id = self.request.GET.get('archivefile')
            ead_id = self.request.GET.get('ead_id')
            deleted_file = self.delete_from_pagebrowser(ead_id=ead_id, archivefile_id=archivefile_id)
            if deleted_file:
                msg = 'Deleted %s - %s -%s' % (ead_id, archivefile_id, deleted_file)
            else:
                msg = 'No archivefile found, not deleted from pagebrowser: %s - %s' % (ead_id, archivefile_id)

            repository_logger.info('[{0}] {1}'.format(now, msg))

            if 'redirect' in request.GET:
                return redirect(urlresolvers.reverse('sync_archivefiles'))
            else:
                return HttpResponse(msg)

        elif 'refresh_all' in request.GET:
            response_msg = ''
            self.published_archivefiles_from_repo = repository.get_archivefiles_with_eads(status=config.STATUS_PUBLISHED, limit=100000)
            for i, archivefile in enumerate(self.published_archivefiles_from_repo):
                if archivefile.status == config.STATUS_PUBLISHED:
                    ead_id = archivefile.ead_id
                    archivefile_id = archivefile.id
                    try:
                        msg = self.publish_in_pagebrowser(ead_id=ead_id, archivefile_id=archivefile_id)
                        repository_logger.info(msg)
                    except Exception, error:
                        msg = ('[%s] [%s/%s] Error: %s' % (now, i, len(self.archivefiles_from_repo), unicode(error)))
                        repository_logger.error(msg)
                    else:
                        msg = ('[%s] [%s/%s] Updated %s - %s' % (now, i, len(self.archivefiles_from_repo), ead_id, archivefile_id))
                        repository_logger.info(msg)
                    response_msg += '{0}\n'.format(msg)

        self.published_archivefiles_from_repo = repository.get_archivefiles_with_eads(status=config.STATUS_PUBLISHED, limit=100000)
        # self.published_archivefiles_from_repo = repository.get_archivefiles_with_eads(limit=100000)

        self.pagebrowser_books = self.get_pagebrowser_books()

        for archivefile in self.published_archivefiles_from_repo:
            pagebrowser_id = archivefile.pagebrowser_id()
            if pagebrowser_id in self.pagebrowser_books:
                archivefile.is_published = True
                archivefile.pagebrowser_last_changed = self.pagebrowser_books[pagebrowser_id].last_changed
            else:
                archivefile.is_published = False
                archivefile.pagebrowser_last_changed = ''


        return super(SyncArchiveFiles, self).get(request, *args, **kwargs)

    def get_archivefile(self, ead_id, archivefile_id):

        if not ead_id:
            ead_id = None
        results = repository.get_archivefiles_with_eads(archivefile_id=archivefile_id)

        if results:
            if ead_id:
                results = [x for x in results if x.ead_id == ead_id]
            if results:
                return results[0]

    def publish_in_pagebrowser(self, ead_id, archivefile_id):
        pagebrowser = self.pagebrowser
        archivefile = self.get_archivefile(ead_id, archivefile_id)
        if archivefile is None:
            msg = u'No archivefile found with {ead_id} and {archivefile_id}: could not publish in pagebrowser'.format(ead_id=ead_id, archivefile_id=archivefile_id)
            repository_logger.warn(msg)
            return msg

        pagebrowser_id = archivefile.pagebrowser_id()

        if ead_id:
            # get the information of this archive file for this ead
            ead_info = repository.open_url(os.path.join(settings.REPOSITORY_PUBLIC_URL, 'ead', ead_id))

            url = os.path.join(settings.REPOSITORY_PUBLIC_URL, 'lists/get_component_for_viewer')
            info = repository.open_url(url, ead_id=ead_id, archiveFile=archivefile.archiveFile)

            if not info['results']:
                msg = u'No archive file "{archivefile.archiveFile}" found in this EAD - tried {url}?ead_id={ead_id}&archiveFile={archivefile.archiveFile}'.format(**locals())
                title = '{archivefile.archiveFile} - {ead_id}'.format(**locals())
                content = 'No information in the EAD file found for this file'
                subtitle = '-'
                language = 'en'
            else:
                info = info['results'][0]

                # from the Finding AID description: Identification, Creator, Title;
                info_findingaid = repository.open_url(url, ead_id=ead_id, xpath='/ead/eadheader/text()[1]')['results'][0]

                info_findingaid_children = dict([(x['xpath'], x) for x in info_findingaid['children']])

                info_findingaid_identification = info_findingaid_children.get('/ead/eadheader/eadid/text()', None)
                info_findingaid_creator = info_findingaid_children.get('/ead/eadheader/eadid/@mainagencycode', None)
                info_findingaid_title = info_findingaid_children.get('/ead/eadheader/filedesc/titlestmt/titleproper/text()', None)

                # from the Archive Introduction: Title, Reference code, Date period, Extent and medium;
                info_introduction = repository.open_url(url, ead_id=ead_id, xpath='/ead/archdesc/did/text()[1]')['results'][0]
                info_introduction_children = dict([(x['xpath'], x) for x in info_introduction['children']])

                info_introduction_title = info_introduction_children.get('/ead/archdesc/did/unittitle/text()', None)
                info_introduction_reference_code = info_introduction_children.get('/ead/archdesc/did/unitid/text()', None)
                info_introduction_date = info_introduction_children.get('/ead/archdesc/did/unitdate/text()', None)
                info_introduction_extent_and_medium = info_introduction_children.get('/ead/archdesc/did/physdesc/extent/text()', None)

                language = ead_info['language']

                subtitle = ''
                subtitle += translate('archiveFile', language) + ': '
                subtitle += info.get('archiveFile')
                archivefile_title = info.get('title', None)
                if archivefile_title:
                    subtitle += ' %s' % archivefile_title

                content = ''

                if info_findingaid:
                    content += '<h2>%s</h2>' % info_findingaid['title']

                if info_findingaid_identification:
                    content += u'<div class="title">%s</div>\n' % info_findingaid_identification['title']
                    content += u'<div class="text">%s</div>\n' % u'<br>'.join(info_findingaid_identification.get('text', []))
                if info_findingaid_creator:
                    content += u'<div class="title">%s</div>\n' % info_findingaid_creator['title']
                    content += u'<div class="text">%s</div>\n' % u'<br>'.join(info_findingaid_creator.get('text', []))

                if info_introduction:
                    content += '<h2>%s</h2>' % info_introduction['title']

                if info_introduction_title:
                    content += u'<div class="title">%s</div>\n' % info_introduction_title['title']
                    content += u'<div class="text">%s</div>\n' % u'<br>'.join(info_introduction_title.get('text', []))
                if info_introduction_reference_code:
                    content += u'<div class="title">%s</div>\n' % info_introduction_reference_code['title']
                    content += u'<div class="text">%s</div>\n' % u'<br>'.join(info_introduction_reference_code.get('text', []))
                if info_introduction_date:
                    content += u'<div class="title">%s</div>\n' % info_introduction_date['title']
                    content += u'<div class="text">%s</div>\n' % u'<br>'.join(info_introduction_date.get('text', []))
                if info_introduction_extent_and_medium:
                    content += u'<div class="title">%s</div>\n' % info_introduction_extent_and_medium['title']
                    content += u'<div class="text">%s</div>\n' % u'<br>'.join(info_introduction_extent_and_medium.get('text', []))

                content += '<h2>%s</h2>' % translate('Archivefile_description', language)
                for attr in [
                    'archiveFile',
                    'title',
                    'scopecontent',
                    'custodhist',
                    # 'text',
                    'description',
                    'date',
                ]:
                    value = info.get(attr, '')
                    if type(value) in types.StringTypes:
                        value = value.replace('\n', '<br />')
                    else:
                        value = '<br />'.join(value)

                    if value.strip():
                        label = translate(attr, language)
                        content += '<div class="title">{label}</div>'.format(label=label)
                        content += '<div class="text">\n'
                        content += value
                    content += '</div>\n'

                if info_findingaid_title:
                    title = ' '.join(info_findingaid_title.get('text', [])),
                else:
                    title = ''

                msg = ''
            show_homePane = True
        else:
            language = 'nl'
            try:
                title = CORPUSDIPLOMATICUMTITLES[int(archivefile.archiveFile) - 1]
            except IndexError:
                msg = 'No known CorpusDipl. title for this archiveFile: {archivefile.archiveFile}'.format(archivefile=archivefile)
                raise Exception(msg)
                title = '-'
            subtitle = ''
            content = ''
            msg = ''
            show_homePane = False

        book = pagebrowser.add_book(
            pagebrowser_id,
            title=title,
        )

        pagebrowser.add_or_update_service_to_book(
            book_id=pagebrowser_id,
            service_url=archivefile.pagelist_url(),
            service_id='1',
        )

        # make default accessor invisible
        book.refresh()
        book.manage_changeAccessor('toc', None, 'off', None)
        book.manage_changeAccessor('search_in_text', None, 'off', None)
        title = translate('thumbnailsPane_title', language)
        book.manage_changeAccessor('thumbnails', title, 'thumbnails_view', {'visible': 'on'})

        title = translate('homePane_title', language)
        if show_homePane:
            visible = 'on'
        else:
            visible = ''
        book.manage_changeView('homePane', title, {'visible': visible, 'url': 'page_view_home'})
        title = translate('imagePane_title', language)
        book.manage_changeView('imagePane', title, {'visible': 'on', 'executeScripts': 'on', 'url': 'page_view_img'})
        book.manage_changeView('pdfPane', 'pdf', {'visible': '', 'url': 'page_view_pdf'})
        book.manage_changeView('htmlPane', 'transcriptie', {'visible': '', 'url': 'page_view_html'})
        book.set_property('subtitle', subtitle, 'string')
        book.manage_moveViewUp('imagePane')

        try:
            book.add_or_update_document('page_view_home', subtitle, content)
        except:
            # TODO: this is a hack - the second time it often works :-(
            book.add_or_update_document('page_view_home', subtitle, content)

        msg += 'refreshed book at %s/%s' % (settings.PAGEBROWSER_URL, pagebrowser_id)
        return msg

    def delete_from_pagebrowser(self, ead_id, archivefile_id):
        pagebrowser = self.pagebrowser
        archivefile = self.get_archivefile(ead_id, archivefile_id)
        if archivefile is not None:
            try:
                pagebrowser.proxy.manage_delObjects([archivefile.pagebrowser_id()], None)
            except Exception, error:
                repository_logger.warn('[1]' + unicode(error))

            return archivefile

    def get_pagebrowser_books(self):
        pagebrowser_books = self.pagebrowser.list_objects(extra_fields=['last_changed'])

        class BookProxy(object):
            def __init__(self, book_id, last_changed):
                self.book_id = book_id
                self.last_changed = last_changed

        books = [BookProxy(b[0], b[1]) for b in pagebrowser_books]
        return dict((book.book_id, book) for book in books)
