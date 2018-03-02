# encoding=utf-8

from settings_local import *


#TEST_ENVIRONMENT to True will make us not use the RealTimeSearchIndex
# (see search_indexes.__init__.py
TEST_ENVIRONMENT = True

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.BaseSignalProcessor'