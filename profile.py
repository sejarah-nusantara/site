import os
import cProfile, pstats, StringIO
from django.conf import settings
import pprint
import sys
THIS_DIR = os.path.join(os.path.dirname(__file__))
sys.path.append(THIS_DIR)
from project import settings_import as default_settings
sortby = 'cumulative'
# sortby = 'tottime'
numlines = 40

DJANGO_SETTINGS_MODULE = 'project.settings'
default_settings.MEDIA_ROOT = os.path.join(THIS_DIR, 'media')
settings.configure(**default_settings.__dict__)
import django
# django.setup()
from dasa.models import Resolution
from dasa.views import RealiaBrowse

from django.test.client import RequestFactory
rf = RequestFactory()
get_request = rf.get('/hello/')
resolution0 = Resolution(date='1801-02-03')
resolution1 = Resolution(date='1727-09-30')
resolution2 = Resolution(date='1744-01-31')

pr = cProfile.Profile()

view = RealiaBrowse()
pr.enable()
view(get_request)
# HERE IS THE FUNCTION TO BE PROFILES
pr.disable()

# format the results and print to stdout
#
s = StringIO.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
stats = s.getvalue()
print '\n'.join(stats.split('\n')[:numlines])
