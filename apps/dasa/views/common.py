#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013-
#


import copy
import os
import random
import json
import types
from datetime import datetime
import logging
from textwrap import dedent

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

import dasa
from dasa import config, models
from dasa import forms
from dasa import queries
from dasa.utils import sluggify, urlencode
from dasa.pagebrowser import PageBrowserBook
from dasa.repository import repository
from dasa.utils import get_page
from dasa.menu import get_menu
from dasa import utils

repository_logger = logging.getLogger('repository.interaction')

LENGTH_OF_RESULTS_LIST = 4

# TODO: these translations should come from the reposiotry (like the others)
_TRANSLATIONS = [
    ('Archivefile_description', 'Archive file description', 'Archiefstuk beschrijving', 'Deskripsi arsip'),
    ('title', 'Title', 'Titel', 'Judul',),
    ('scopecontent', 'Scope and content', 'Bereik en inhoud', 'Ruang Lingkup dan Isi',),
    ('description', 'Description', 'Beschrijving', 'Deskripsi'),
    ('date', 'Date period', 'Datum(s)', 'Kurun Waktu'),
    ('view_the_archive_file', 'View the archive file', 'Toon het archiefstuk', 'Lihat berkas arsip'),
    ('archiveFile', 'Archive File', 'Archiefbestand', 'Archive File',),
    ('homePane_title', 'Archival Description', 'Archiefbeschrijving', 'Deskripsi arsip'),
    ('imagePane_title', 'Images', 'Afbeeldingen', 'Gambar'),
    ('thumbnailsPane_title', 'Thumbnails', 'Thumbnails', 'Thumbnails'),
    ('custodhist_header', 'Archival history', 'Archiefhistorie', 'Sejarah Arsip',),
    ('custodhist', 'Archival history', 'Archiefhistorie', 'Sejarah Arsip',),
]


TRANSLATIONS = {}

for k, en, nl, ind in _TRANSLATIONS:
    TRANSLATIONS[k] = dict(en=en, nl=nl, id=ind)


def translate(phrase, language):
    return TRANSLATIONS[phrase][language]


def admin_link(page):
    if page:
        return urlresolvers.reverse('admin:dasa_%s_change' % page._meta.module_name, args=[page.pk])


def prettyprint_query(query, form):
    query_pp_items = []
    for k, v in query.items():
        if not v:
            continue
        if k in ['page', 'order_by']:
            continue
        if k in form.base_fields:
            label = form.base_fields[k].label
            query_pp_items.append(u' <em>{label}</em> is <em>{v}</em> \n'.format(v=v, label=label))  # .lower())
    result = ' and '.join(query_pp_items)
    result = result.strip()
    result = mark_safe(result)
    return result


def _tagcloud(tags, size=20, font_size=15):
    """given a set of tags (pairs of (string, number_of_occurrences)

    arguments:
    - size: the number of tags returned [approx - it takes font_size into account as swell]
    - font_size: the (maximum) font size of the tags)

    return  random subset of size of (string, font-size)
    """
    # XXX next code is the same as in RealiaSearch.extra_context; need to refactor
    random.shuffle(tags)
    font_size = float(font_size)
    cntr = 0

    # tags_to_show = []
    # for tag, count in tags:
    #     cntr += count
    #     tags_to_show.append((tag, count))
    #     if cntr > target:
    #         break
    tags = tags[:size]

    # instead of counts, we create font-sizes
    counts = [count for _x, count in tags]
    if not counts:
        return []
    counts.sort()
    min_count, max_count = counts[0], counts[-1]
    diff = float(max_count - min_count)
    if diff == 0:
        diff = 1
    tags = [(subject, font_size + (float(count) * (font_size / float((diff))))) for subject, count in tags]
    # if we have loots of bigs tags, we remove some
    tags_to_show = []
    total_size = 0
    total_size_target = font_size * size
    for (tag, size) in tags:
        total_size += size
        tags_to_show.append((tag, str(size)))
        if total_size > total_size_target:
            break
    # tags_to_show.append(('{total_size}/{total_size_target}'.format(**locals()), str(font_size)))

    return tags_to_show


class Page(TemplateView):
    """Base class for all pages on the site"""
    slug = None
    readmore_buttons = False  # if the text is very long, hide extra paragrapsh behing 'read more' buttons

    def dispatch(self, *args, **kwargs):
        self._set_path_and_page(*args, **kwargs)
        return super(Page, self).dispatch(*args, **kwargs)

    def _set_path_and_page(self, *args, **kwargs):
        self._kwargs = kwargs
        self.path = kwargs.get('path', None)
        try:
            self.page = self.get_page(self.path)
        except Exception as error:
            raise error

    @property
    def template_name(self):
        # if we have a template of the currently requested path, we use that
        # instead of the standard 'basicpage.html'
        if hasattr(self, 'kwargs'):
            path = self.kwargs.get('path', '')
        else:
            path = None
        if path:
            template_name = '%s.html' % path
        if self.slug:
            template_name = '%s.html' % self.slug
        template_dir = os.path.join(os.path.dirname(dasa.__file__), 'templates')
        template_fullpath = os.path.join(template_dir, 'pages', template_name)
        if os.path.exists(template_fullpath):
            return os.path.join('pages', template_name)

        if getattr(self.page, 'ead', None):
            return 'eadpage.html'

        # if we did not find a custom template, we return the standard one
        if getattr(self, '_template_name', None):
            return self._template_name

        return 'basicpage.html'

    def get_page(self, path=None):
        """try to find a BasicPage object with a slug corresponding to path or self.slug"""
        if path:
            slug = path
        else:
            slug = self.slug
        if slug:
            return get_page(slug)

    def get_menu(self):
        if hasattr(self.request, 'MENU'):
            return self.request.MENU
        else:
            menu = get_menu()
            self.request.MENU = menu
            return menu

    def breadcrumbs(self):
        path = self.request.path
        path = path.replace('/id/', '/')
        # TODO: optimization: recreating the menu each time is expensive - and it is not clear why we need to..
        breadcrumbs = self.get_menu().get_breadcrumbs(slug=path, context_stack=[])
        breadcrumbs = [(x.page.title, x.get_absolute_url()) for x in breadcrumbs]
        if breadcrumbs and breadcrumbs[-1][1] == self.request.path:
            breadcrumbs = breadcrumbs[:-1]
        return breadcrumbs

    def meta_keywords(self):
        result = getattr(self.page, 'meta_keywords', '') or ''
        # get keywords for all pages
        for key in ['all', type(self.page).__name__]:
            for metatag in models.MetaTags.objects.filter(object_type=key):
                if metatag.keywords:
                    result += ' ' + metatag.keywords

        result = result.strip()
        return result

    def meta_description(self):
        result = getattr(self.page, 'meta_description', '') or ''
        if not result:
            result = getattr(self.page, 'title', '')
        for key in ['all', type(self.page).__name__]:
            for metatag in models.MetaTags.objects.filter(object_type=key):
                if metatag.description:
                    result += ' ' + metatag.description
        result = result.strip()
        return result

    def get_context_data(self, path=None, **kwargs):
        page = self.page
        breadcrumbs = self.breadcrumbs()

        context = {
            'path': path,
            'page': page,
            'home_page': get_page('home'),
            'admin_link': admin_link(page),
            'breadcrumbs': breadcrumbs,
            'menuitems': self.get_menu().menuitems(breadcrumbs + [self.request.path]),
            'google_analytics_id': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
            'meta_description': self.meta_description(),
            'meta_keywords': self.meta_keywords(),
            'readmore_buttons': self.readmore_buttons,
        }
        for key in config.__dict__:
            if key.startswith('SLUG_'):
                context[key] = config.__dict__[key]

        if getattr(self.page, 'ead', None):
            # language = self._kwargs['language']
            language = 'en'
            view_archivefile_text = translate('view_the_archive_file', language)
            custodhist_header = translate('custodhist_header', language)

            pagebrowser_url = settings.PAGEBROWSER_PUBLIC_URL
            repository_url = settings.REPOSITORY_PUBLIC_URL
            if not repository_url.endswith('/'):
                repository_url += '/'

            context.update({
                'ead_id': self.page.ead,
                'pagebrowser_url': pagebrowser_url,
                'repository_url': repository_url,
                'view_archivefile_text': view_archivefile_text,
                'custodhist_header': custodhist_header,
            })
        return context


    def get_context_order_by(self, fld_names, default=None):
        """a helper function for making orderable tables

        return a dictiontary with:
            'order_by' a fieldname (based on self.request and default
            'url_order_by_%(field_name)' for each name in fld_names
        """
        if not isinstance(default, type([])):
            default = [default]

        query = dict(self.request.REQUEST)

        order_by = self.request.GET.get('order_by', None)
        if not order_by:
            order_by = default
        if order_by:
            if not isinstance(order_by, type([])):
                order_by = [order_by]
        else:
            order_by = []

        context = {}
        qs = context.get('qs', {})
        for fld_name in fld_names:
            order_by_fld_name = fld_name
            if fld_name in order_by:
                order_by_fld_name = '-%s' % order_by_fld_name
            q = copy.copy(query)
            q['order_by'] = order_by_fld_name
            qs['order_by_%s' % fld_name] = urlencode(q)

        context['order_by'] = order_by
        context['qs'] = qs

        return context

    def navigation_context(self, paginator, page):
        """return a dictionary with values to add to the context to use constructing page navigation links"""
        page_number = page.number
        query = dict(self.request.REQUEST)
        q = copy.copy(query)

        q.update({'page': unicode(page_number + 1)})
        qs_next = urlencode(q)

        q = copy.copy(query)
        q.update({'page': unicode(page_number - 1)})
        qs_prev = urlencode(q)

        last_page = paginator.page_range[-1]
        q = copy.copy(query)
        q.update({'page': unicode(last_page)})
        qs_last = urlencode(q)

        q = copy.copy(query)
        q.update({'page': unicode(1)})
        qs_first = urlencode(q)

        q = copy.copy(query)
        if 'page' in q:
            del q['page']
        qs_nopage = urlencode(q)

        context = {
            'qs_next': qs_next,
            'qs_prev': qs_prev,
            'qs_last': qs_last,
            'qs_first': qs_first,
            'qs_nopage': qs_nopage,
            'paginator_page': page,
            'paginator': paginator,
        }
        return context


class DasaSearchView(Page, SearchView):
    """A mixin-class for searching objects in the database"""
    results_per_page = 20
    _template_name = 'search/search.html'
    slug = 'search'
    orderable_fields = ['date', 'description', 'subject', 'source']

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        SearchView.__init__(self, *args, **kwargs)
        try:
            self._set_path_and_page(*args, **kwargs)
        except Http404:
            self.page = None
        self.form_class = forms.SiteSearchForm

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.

        unfortunately, we use the 'page' variable for the model/page that is shown
        while haystack uses 'page' for representing a paged set of results
        so we copy the code from django_haystack and make use the variable 'paginator_page' instead
        """
        paginator, page = self.build_page()
        context = self.navigation_context(paginator, page)

        context.update({
            'query': self.query,
            'form': self.form,
            'suggestion': None,
        })

        if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
            context['suggestion'] = self.form.get_suggestion()
        context.update(self.extra_context())
        if self.slug:
            context['page'] = self.get_page(self.slug)
        return render_to_response(self.template_name, context, context_instance=self.context_class(self.request))

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            qry = self.form.cleaned_data
            return qry
        return ''

    def save_session(self):
        """we save the query data in the session object """
        # but do we actually use this anywhere?
        formdata = self.get_query() or {}
        try:
            self.request.session['formdata'] = formdata
        except AttributeError:
            pass

    def build_page(self):
        """
        Paginates self.results appropriately.

        there are two parameters in the request that determine which part of the list is shown:
            page: which page of the results will be shown
            selected: which result will be selected

        if page is given, and selected is not, then we will try to show the page on which selected is shown
        """
        # extract the parameters from the request, and do some simple validation
        page_no = self.request.GET.get('page', None)
        if page_no:
            try:
                page_no = int(page_no)
            except (TypeError, ValueError):
                page_no = None

            if page_no and page_no < 1:
                page_no = None

        selected_order = self.request.GET.get('selected')
        if selected_order:
            try:
                selected_order = int(selected_order)
            except (TypeError, ValueError):
                raise Http404("Not a valid number for 'selected'.")

        paginator = Paginator(self.results, self.results_per_page)

        if page_no:
            start_offset = (page_no - 1) * self.results_per_page
            try:
                page = paginator.page(page_no)
            except InvalidPage:
                page = paginator.page(paginator.num_pages)
        elif selected_order:
            # try to find the page where the result with this position is on
            # offset shows the selected resutl in the 3d position
            start_offset = selected_order - 3
            start_offset = max(start_offset, 0)
            page_no = int(start_offset / self.results_per_page) + 1
            object_list = self.results[start_offset:start_offset + self.results_per_page]
            page = PaginatorPage(object_list, page_no + 1, paginator)
        else:
            page_no = 1
            selected_order = 0
            page = paginator.page(page_no)
            start_offset = 0

        return (paginator, page)

    def extra_context(self):
        request = self.request
        query = dict(request.REQUEST)
        context = Page.get_context_data(self, self.slug)

        req_order_by = query.get('order_by')

        # construct query string
        for order_by in self.orderable_fields:
            q = copy.copy(query)
            if req_order_by == order_by:
                q['order_by'] = u'-%s' % order_by  # sort descending
            else:
                q['order_by'] = order_by  # sort ascending

            context.update({
                'qs_order_by_%s' % order_by: urlencode(q),
            })

        query_prettyprinted = ''

        for k, v in query.items():
            if v and k not in ['page', 'order_by']:
                query_prettyprinted += u'%(k)s is <em>%(v)s</em>\n' % locals()
        query_prettyprinted += ''

        context['query_prettyprinted'] = query_prettyprinted.strip()

        selected_order = self.request.GET.get('selected')
        if selected_order and selected_order.isdigit():
            context['selected_order'] = int(selected_order)

        # save the query data in the session, so its stays accessable
        self.save_session()
        return context
