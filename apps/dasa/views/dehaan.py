
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

import userena
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

from common import DasaSearchView, Page, translate, admin_link, prettyprint_query, _tagcloud


class DeHaanBrowse(DasaSearchView):
    slug = config.SLUG_DEHAAN_BROWSE
    template_name = 'pages/dehaan-browse.html'
    # orderable_fields = ['archive_reference', 'date', 'title', 'vessel_names', ]

    def __init__(self, *args, **kwargs):
        DasaSearchView.__init__(self, *args, **kwargs)
        self.form_class = forms.DeHaanSearchForm

    def extra_context(self):
        context = super(DeHaanBrowse, self).extra_context()
        # context.update(self.get_context_order_by(self.orderable_fields, default='archive_reference'))
        # published_archivefiles = repository.get_archivefiles(status=config.STATUS_PUBLISHED)
        # context['published_archivefiles'] = [x.archiveFile for x in published_archivefiles]
        return context

    def build_page(self):
        paginator, page = super(DeHaanBrowse, self).build_page()
        return (paginator, page)


class DeHaanSearch(DeHaanBrowse):
    slug = config.SLUG_DEHAAN_SEARCH
    template_name = 'pages/dehaan-search.html'

    def extra_context(self):
        context = super(DeHaanSearch, self).extra_context()

        context['tags_indexTerms'] = _tagcloud(queries.get_dehaan_indexTerms())

        query = dict(self.request.REQUEST)
        query_prettyprinted = prettyprint_query(query=query, form=self.form_class)
        context['query_prettyprinted'] = query_prettyprinted
        return context


class DeHaanIndexMap(Page):
    slug = config.SLUG_DEHAAN_INDEXTERMS
    template_name = 'pages/dehaan-indexmaps.html'
    readmore_buttons = False

    def get_context_data(self, **kwargs):
        context = {}
        context = super(DeHaanIndexMap, self).get_context_data()
        first_letter = self.request.REQUEST.get('first_letter')
        vessel_names = queries.get_dehaan_indexTerms()

        def _sort_string(vessel_name):
            """a string used for sorting
            """
            s = vessel_name
            s = s.strip()
            for prefix in ['de ', "'t ", "l'", "'s "]:
                if s.startswith(prefix):
                    s = s[len(prefix):]
            s = s + vessel_name
            return s.lower().strip()

        vessel_names = [(_sort_string(name), name, count) for name, count in vessel_names]

        letters_and_counts = [
            (letter, len([s for s in vessel_names if s[0].upper().startswith(letter)])) for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()
        ]
        letters_and_counts = [(x, c) for x, c in letters_and_counts if c > 0]

        letters_and_counts.append(('All', len(vessel_names)))

        if first_letter and first_letter.lower() != 'all':
            vessel_names = [(sort_string, name, c) for sort_string, name, c in vessel_names if sort_string.startswith(first_letter.lower())]
        vessel_names.sort()
        vessel_names = [('%s' % name, c) for _sort_string, name, c in vessel_names]

        # make three columns
        col_length = len(vessel_names) / 3 + 1
        vessel_names = [vessel_names[:col_length], vessel_names[col_length: 2 * col_length], vessel_names[2 * col_length:]]

        context.update({
            'index_terms': vessel_names,
            'letters': letters_and_counts,
        })
        return context
