# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#


import os
import sys
from basic_tests import *
from haystack import indexes


class SiteSearchIndex(indexes.SearchIndex):
    """

    "The RealTimeSearchIndex provides all the same functionality as the standard SearchIndex. However, in addition, it connects to the post_save/post_delete signals of the model it’s registered with."
    http://django-haystack.readthedocs.org/en/latest/searchindex_api.html#realtimesearchindex
    """
    text = indexes.CharField(document=True, model_attr='solr_index')
