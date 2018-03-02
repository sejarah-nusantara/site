# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#


from dasa.menu import Menu
from dasa import config
from dasa.models import HartaKarunMainCategory
from dasa import models

from basic_tests import BaseTestCase


class MenuTestCase(BaseTestCase):

    def setUp(self):
        super(MenuTestCase, self).setUp()
        self.assert_order_is_sane()
        self.add_page('m1_2_1')
        self.menuitem1_2_1 = self.add_menuitem('m1_2_1', self.menuitem1_2)
        self.assert_order_is_sane()
        self.add_page('m1_2_2')
        self.menuitem1_2_2 = self.add_menuitem('m1_2_2', self.menuitem1_2)
        self.assert_order_is_sane()

        self.add_page('m1_1_1')
        self.menuitem1_1_1 = self.add_menuitem('m1_1_1', self.menuitem1_1)
        self.assert_order_is_sane()
        self.add_page('m1_1_2')
        self.menuitem1_1_2 = self.add_menuitem('m1_1_2', self.menuitem1_1)
        self.test_sanity_of_menu()

        # also give some names so we understand debug traces better
        for att in dir(self):
            if att.startswith('menuitem'):
                menuitem = getattr(self, att)
                if menuitem.page.title.startswith('menuitem'):
                    continue
                menuitem.page.title = att
                menuitem.page.save()
        self.refresh_menuitem_attributes()

    def get_menuitem(self, menuitem_id):
        return models.MenuItem.objects.get(id=menuitem_id)

    def refresh_menuitem_attributes(self):
        for att in dir(self):
            if att.startswith('menuitem'):
                setattr(self, att, self.get_menuitem(getattr(self, att).id))

    def assert_order_is_sane(self):
#         menuitems = models.MenuItem.objects.all()
#         order_numbers = [menuitem.order for menuitem in menuitems]
#         # assert that there are no dupblicates
        msg = [(x, x.order) for x in models.MenuItem.objects.order_by('order')]
        self.assertEqual([x.order for x in models.MenuItem.objects.order_by('order')], range(1, models.MenuItem.objects.count() + 1), msg)

    def test_sanity_of_menu(self):
        # assert that the menu is like it was just after setup
        self.refresh_menuitem_attributes()

        self.assert_order_is_sane()

        self.assertEqual(self.menuitem1.position, 1)
        self.assertEqual(self.menuitem1_1.position, 1)
        self.assertEqual(self.menuitem1_1_1.position, 1)
        self.assertEqual(self.menuitem1_1_2.position, 2)
        self.assertEqual(self.menuitem1_2.position, 2)
        self.assertEqual(self.menuitem1_2_1.position, 1)
        self.assertEqual(self.menuitem1_2_2.position, 2)
        self.assertEqual(self.menuitem2.position, 2)
        self.assertEqual(self.menuitem3.position, 3)

        self.assertEqual(self.menuitem1.order, 1)
        self.assertEqual(self.menuitem1_1.order, 2)
        self.assertEqual(self.menuitem1_1_1.order, 3)
        self.assertEqual(self.menuitem1_1_2.order, 4)
        self.assertEqual(self.menuitem1_2.order, 5)
        self.assertEqual(self.menuitem1_2_1.order, 6)
        self.assertEqual(self.menuitem1_2_2.order, 7)
        self.assertEqual(self.menuitem2.order, 8)
        self.assertEqual(self.menuitem3.order, 9)

    def test_reorder_menuitems(self):
        # menuitem1_1 as two children, so the offset after reordering its children should be increment by 2
        self.assertEqual(models.MenuItem.reorder_menuitems(parent=self.menuitem1_1, offset=1), 1 + 2)
        models.MenuItem.reorder_menuitems()
        self.assertEqual(models.MenuItem.objects.get(id=self.menuitem1_1.id).order, 2)
        self.assert_order_is_sane()

    def test_move_menuitems(self):
        # cf test_sanity_of_menu for the original order
        menuitems = models.MenuItem.objects.filter(parent=None).all()
        # get some menuitem with children
        menuitem1 = menuitems[0]
        menuitem1_1 = menuitem1.children()[0]
        # for saniy, we check that our parent has exactly two chidlren
        self.assertEqual(len(menuitem1.children()), 2)

        # trying to move the first menuitem one level up has no effect
        self.assertEqual(menuitem1_1.position, 1)
        menuitem1_1.move_menuitem(-1)
        self.assertEqual(menuitem1_1.position, 1)
        self.assert_order_is_sane()
        self.test_sanity_of_menu()

        # moving it down, hower, changes its position
        self.assert_order_is_sane()
        menuitem1_1.move_menuitem(1)
        self.assertEqual(menuitem1_1.position, 2)
        self.refresh_menuitem_attributes()
        self.assertEqual(self.menuitem1.order, 1)
        self.assertEqual(self.menuitem1_2.order, 2)
        self.assertEqual(self.menuitem1_2_1.order, 3)
        self.assertEqual(self.menuitem1_1.order, 5)
        self.assertEqual(self.menuitem2.order, 8)
        self.assertEqual(self.menuitem1.children(), [self.menuitem1_2, self.menuitem1_1])
        self.assert_order_is_sane()
        # this is the last position - moving down again has no effect
        menuitem1_1.move_menuitem(1)
        self.assertEqual(menuitem1_1.position, 2)
        self.assert_order_is_sane()

        # now we move it up again
        menuitem1_1.move_menuitem(-1)
        self.assertEqual(menuitem1_1.position, 1)

        # everything should now be as before
        self.test_sanity_of_menu()

    def test_manipulation_of_menuitems(self):
        menuitems = models.MenuItem.objects.filter(parent=None).all()
        # get some menuitem with children
        menuitem1 = menuitems[0]
        menuitem1_1 = menuitem1.children()[0]
        # now give menuitem1_1 another parent
        menuitem2 = menuitems[1]
        menuitem1_1.parent = menuitem2
        menuitem1_1.save()

        self.assertTrue(menuitem1_1 not in menuitem1.children())
        self.assertTrue(menuitem1_1 in menuitem2.children())
        self.assertEqual(menuitem1_1.position, len(menuitem2.children()))

        models.MenuItem.reorder_menuitems()
        menuitem2 = models.MenuItem.objects.get(id=menuitem2.id)
        self.assertEqual(menuitem1_1.order, menuitem2.order + len(menuitem2.children()))

    def test_menu_definition(self):
        """check if the menu is well-defined"""
        menu = Menu()
        menuitems = menu.menuitems('/')
        # of which we should have more than 3
        # the first one is hte hartakarun one
        # the first one is the hartakarun menu
        hartakarun_menuitem = menuitems[2]
        self.assertEqual(hartakarun_menuitem.url, '/hartakarun/')
        # it has 4 children (the main categories), plus the list of all articles
        self.assertEqual(len(hartakarun_menuitem.children), 4 + 1)

        # and each main categories has 6 subcategiers
        self.assertEqual(len(hartakarun_menuitem.children[2].children), 6)

    def assertEqual_menuitems(self, ls1, ls2):
        self.assertEqual([m.page.id for m in ls1], [m.page.id for m in ls2])

    def test_show_submenu(self):
        """test if the menu folds out when it should """

#        self.assertTrue('x' in MENUSTRUCTURE, MENUS)
        menu = Menu()
        # by default, we should have the menuitems of the root

        self.assertEqual_menuitems(menu.menuitems('/'), menu.menuitems())
        # in fact, the menu does not depend on the url
        self.assertEqual_menuitems(menu.menuitems('/some_invented_url/'), menu.menuitems())

        # what changes is which submenu is shown
        # if we ask for he menuitems of that url, we should get its children
        self.assertEqual(menu.menuitems()[0].url, '/foreword/')
        self.assertEqual(menu.menuitems()[2].url, '/hartakarun/')
        # on the url /hartakarun, the third menuitem (= the hartakarun submenu) should be folded open
        self.assertEqual(menu.menuitems('/hartakarun/')[2].show_submenu(), True)
        self.assertEqual(menu.menuitems('/someotherurl/')[0].show_submenu(), False)

        # check if all children get their path set correctly
        self.assertEqual(menu.menuitems('/some_url/')[2].children[1].path, ['/some_url/'])
        # if we aks for the url of the second main category, then we should see IT's submenu
        second_main_category = HartaKarunMainCategory.objects.all()[1]
        second_main_category_url = second_main_category.get_absolute_url()

        self.assertEqual(menu.menuitems(second_main_category_url)[2].children[2].url, second_main_category_url)
        self.assertEqual(menu.menuitems(second_main_category_url)[2].children[2].show_submenu(), True)

        # a detail page of the resolutions should  have the archive and resolution books with submenus
        menuitems = menu.menuitems('/%s/5/' % config.SLUG_ARCHIVE_GENERALRESOLUTIONS)
        # get the 'archive' submenu
        for item in menuitems:
            if item.get_absolute_url() == '/%s/' % config.SLUG_ARCHIVE:
                item_archive = item
        # the submenu should show
        self.assertEqual(item_archive.show_submenu(), True)

    def test_language(self):
        # get a page in indonesian
        response = self.app.get('/hartakarun/')
        self.assertNotContains(response, 'href="/id/archive/"')
        response = self.app.get('/id/hartakarun/')
        self.assertContains(response, 'href="/id/archive/"')

    def test_defined_slugs(self):
        """tests if there are pages available for each slug defined in json.py"""
        slugs = [getattr(config, c) for c in config.__dict__ if c.startswith('SLUG_')]
        # the following slugs do not have basicpage objects
        exclude = ['hartakaruncategory', 'hartakarunmaincategory']
        slugs = [slug for slug in slugs if slug not in exclude]
        notfound = []
        for slug in slugs:
            try:
                try:
                    models.BasicPage.objects.get(slug=slug)
                except Exception, error:
                    print slug
                    raise Exception('%s when getting %s' % (error, slug))
            except models.BasicPage.DoesNotExist:
                notfound.append(slug)
        if notfound:
            raise Exception('The following slugs could not be found: %(notfound)s' % locals())

        for slug in slugs:
            self.client.get('/%s/' % slug)
