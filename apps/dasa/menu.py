import copy
import types
import logging

from django.core.urlresolvers import reverse

from dasa import models
from dasa import config

logger = logging.getLogger()


def _(s):
    return s


def get_page(slug):
    try:
        return models.BasicPage.objects.get(slug=slug)
    except models.BasicPage.DoesNotExist as error:
        logger.error(unicode(error))
        return None


class MenuItem:
    """An item in the menu

    """
    def __init__(self, slug=None, page=None, children=[], path=None, title=None, url=None):
        """
        arguments:

        """

        self._slug = slug
        if page:
            self.page = page

        elif slug:
            self.page = get_page(slug)
            if not self.page:
                self._title = slug
        else:
            self.page = None

        self.children = children
        self._title = title
        self._url = url

    @property
    def title(self):
        if self._title:
            return self._title
        elif self.page:
            if hasattr(self.page, 'extended_title'):
                return self.page.extended_title
            else:
                return self.page.title
        else:
            return self._slug

    @property
    def url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        if self._url:
            return self._url
        if not self.page:
            #
            return '/%s' % self._slug
        url_name = self.page._meta.module_name
        if url_name == 'basicpage':
            args = [self.page.slug]
        else:
            args = [self.page.pk]
        url = reverse(url_name, args=args)
        return url

    def __unicode__(self):
        return '<MenuItem Instance %s [%s]>' % (self.title, self.children)

    def __str__(self):
        return self.__unicode__()

    def show_submenu(self):
        if self.is_selected():
            return True
        # a special case: we open the submenu 'entries' if we are looking at the archive page
        if '/archive/' in self.path and self._slug == 'entries':
            return True
        if self._slug == config.SLUG_ARCHIVE and unicode(self.path[-1].startswith('/hath')):
            return True
        return False

    def is_selected(self):
        if self.get_absolute_url() in self.path:
            return True

        for x in self.children:
            if x.is_selected():
                return True

#     def get_all_children(self):
#         """get children recursively"""
#         result = copy.deepcopy(self.children)
#         for x in self.children:
#             x.parent = self
#             result += x.get_all_children()
#         return result


class Menu(object):
    """The navigation menu menu"""
    def __init__(self):
        self._menuitems = None

    def menuitems(self, path=None):
        """get the menuitems folded out depending on the paths (which is a list of local paths)

        arguments:
            path: a list of paths
        """

        if type(path) in types.StringTypes:
            path = [path]

        for menuitem in self.get_menuitems():
            menuitem.path = path
            for c in menuitem.children:
                c.path = path
                for cc in c.children:
                    cc.path = path
                    for ccc in cc.children:
                        ccc.path = path
                        for cccc in ccc.children:
                            cccc.path = path
        return self.get_menuitems()

    def get_menuitems(self):

        if self._menuitems is None:
            self._menuitems = self._menustructure()
        return self._menuitems

    def refresh(self):
        """reset all cached data"""
        self._menuitems = None

    def _menustructure(self, menuitems=None):
        if menuitems is None:
            menuitems = models.MenuItem.objects.filter(parent=None).select_related('page').order_by('position').all()

        def get_children(menuitem):
            children = self._menustructure(menuitem.children())
            if menuitem.page.slug == config.SLUG_HARTAKARUN:
                children += self._create_hk_submenu()
            return children

        return [MenuItem(slug=menuitem.page.slug, page=menuitem.page, children=get_children(menuitem)) for menuitem in menuitems]
        return [MenuItem(page=menuitem.page, children=get_children(menuitem)) for menuitem in menuitems]

    def get_breadcrumbs(self, slug, context_stack=[], items=[]):
        slug = slug.strip('/')
        if not items:
            items = self.get_menuitems()
        for menuitem in items:
            context_stack.append(menuitem)
            if menuitem._slug == slug:
                return context_stack
            elif menuitem._slug == config.SLUG_DAILY_JOURNALS_VOLUMES and (slug.startswith('hathi') or slug.startswith('id/hathi')):
                # all pages with a slug starting with '/hathi' (or /id/hathi)
                # are part of the daily_journal_volums section
                return context_stack
            elif menuitem._slug == config.SLUG_NEWS and menuitem._slug in slug:
                return context_stack
            elif menuitem.children:
                bc = self.get_breadcrumbs(slug, context_stack, menuitem.children)
                if bc:
                    return bc
            context_stack.remove(menuitem)
        return []

    def _create_hk_submenu(self):
        hk_main_categories = models.HartaKarunMainCategory.objects.all()

        def hk_subcategories(hk_main_category):
            return [MenuItem(page=x) for x in hk_main_category.subcategories.all()]

        return [MenuItem(slug=config.SLUG_HARTAKARUN_ALL_ARTICLES)] + \
            [MenuItem(page=x, children=hk_subcategories(x)) for x in hk_main_categories]


def get_menu():
    return Menu()
