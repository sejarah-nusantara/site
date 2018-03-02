# encoding=utf-8
#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013
#

from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from basic_tests import BaseTestCase
from dasa import config

context = config.__dict__


class GroupsTestCase(BaseTestCase):
    """test if all groups can see what they need to see"""
    _password = 'test'

    def setUp(self):
        super(GroupsTestCase, self).setUp()
        self._editors_group = Group.objects.get(name='Web Editors')
        permission_to_change = Permission.objects.get(codename='change_basicpage')
        self._editors_group.permissions.add(permission_to_change)
        self._editors_group.save()

    def _create_user(self, groups=[]):
        user = User.objects.create_user('test_user', 'test@example.com', self._password)
        user.is_staff = True
        for group_name in groups:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        user.save()
        return user

    def assertHasEditLink(self, response):
        return self.assertContains(response, 'edit this page')

    def assertNotHasEditLink(self, response):
        return self.assertNotContains(response, 'edit this page')

    def test_superuser_can_edit(self):
        """test if the superuser has an edit link on the right pages"""
        # the superuser should see eidt links on all pages. we test some that have gone awry in development
        user = self.superuser
        assert self.client.login(username=user.username, password=self._password)

        self.assertHasEditLink(self.client.get('/%(SLUG_NEWS)s/' % context))
        self.assertHasEditLink(self.client.get('/%(SLUG_HARTAKARUN)s/' % context))
        self.assertHasEditLink(self.client.get('/%(SLUG_SEARCH)s/' % context))
        self.assertHasEditLink(self.client.get('/hartakarun/item/3/' % context))

    def test_anonymous_users(self):
        # anonymous users should have no edit link
        self.assertNotHasEditLink(self.client.get('/%(SLUG_NEWS)s/' % context))
        response = self.app.get('/%(SLUG_NEWS)s/' % context)
        self.assertNotHasEditLink(response)

    def test_web_editors(self):
        """web editors should have edit links on all editable pages"""
        # create a web editor
        user = self._create_user(groups=['Web Editors'])

        # first test sanity
        self.assertTrue(user.has_perm('dasa.change_basicpage'))

        response = self.app.get('/%(SLUG_NEWS)s/' % context, user=user.username)
        perms = response.context[0]['perms']
        self.assertTrue(perms['dasa']['change_basicpage'])
        self.assertFalse(perms['dasa']['change_user'])

        # login
        response = self.client.login(username=user.username, password=self._password)
        # make sure our login is successful
        self.assertTrue(response)
        self.assertHasEditLink(self.client.get('/%(SLUG_NEWS)s/' % context))
        self.assertHasEditLink(self.client.get('/%(SLUG_HARTAKARUN)s/' % context))
        self.assertHasEditLink(self.client.get('/%(SLUG_SEARCH)s/' % context))
        self.assertHasEditLink(self.client.get('/hartakarun/item/3/' % context))

        # the webeditor should be able to access the admin interface
        response = self.client.get('/admin/')
        self.assertContains(response, 'DASA Admin')
