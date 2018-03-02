#create_pagebrowser_books
from optparse import make_option
from django.core.management.base import BaseCommand
from dasa import pagebrowser


class Command(BaseCommand):
    help = "Creates (or initializes) pagebrowser books for the data in the database."
    base_options = (
        make_option("-f", "--filename", action="store", type="string", dest="filename",
                    help='If provided, directs output to a file instead of stdout.'),
    )
    option_list = BaseCommand.option_list + base_options

    def handle(self, **options):
        """create (or update) books in the pagebrowser"""
        raise Exception("""This is not working at the moment, and it will be replaced
        by anb admin screen (at admin/retrobooks)""")
        print 'yes'
        USER = 'admin'
        PASSWORD = 'admin'
        #XXX get these data from buildout.cfg
        url = "http://%(USER)s:%(PASSWORD)s@%(PAGEBROWSER_URL)s" % locals()
        pb = pagebrowser.PageBrowser(url)
        pagebrowser.add_resolution_book(pb)
#        pagebrowser.add_hartakarun_articles(pb)
        pagebrowser.add_retrobooks(pb)

        return
