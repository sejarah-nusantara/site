from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard


class MyDashboard(Dashboard):
    def __init__(self, **kwargs):

        # append an app list module for "Applications"
        super(MyDashboard, self).__init__(**kwargs)
        self.children.append(modules.AppList(
            title=_('Applications'),
            column=1,
            collapsible=True,
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title=_('Administration'),
            column=1,
            collapsible=True,
            models=('django.contrib.*',),
        ))

        # append another link list module for "support".
#         self.children.append(modules.LinkList(
#             _('Translation'),
# #             title_url= reverse('rosetta-home'), #does not seem to do anything
#             column = 1,
#             children=[
# #                {
# #                    'title': _('Rosetta'),
# #                    'url': reverse('rosetta-home'),
# #                    'external': False,
# #                },
#                 {
#                     'title': _('Translate phrases on website'),
#                     'url': '%spick/?filter=third-party' % reverse('rosetta-home'),
#                     'external': False,
#                 },
#
#             ],
#             collapsible=True,
#         ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Syncing between repository and pagebrowser'),
            column=1,
            children=[

                {
                    'title': _('Synchronize Archivefiles'),
                    'url': 'sync_archivefiles',
                    'external': False,
                },

            ],
            collapsible=True,
        ))

        # link to filebrowser
        self.children.append(modules.LinkList(
            _('Filebrowser'),
            column=1,
            children=[

                {
                    'title': _('Browse'),
                    'url': './filebrowser/browse/',
                    'external': False,
                },

            ],
            collapsible=True,
        ))

        # append a recent actions module
        self.children.append(modules.LinkList(
            _('Web site'),
            title_url='/',  # does not seem to do anything
            column=2,
            children=[
#                {
#                    'title': _('Rosetta'),
#                    'url': reverse('rosetta-home'),
#                    'external': False,
#                },
                {
                    'title': _('Go to web site'),
                    'url': '/',
                    'external': False,
                },

            ],
            collapsible=True,
        ))
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            column=2,
            collapsible=False,
            limit=5,
        ))
