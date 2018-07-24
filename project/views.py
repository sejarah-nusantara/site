
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from dasa import models
from dasa.menu import MenuItem, get_page
from dasa import config


def base_html(request):
    context = {}
    return render(request, 'base.html', context)
