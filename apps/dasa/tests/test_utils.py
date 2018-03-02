#
# copyright Gerbrandy SRL
# www.gerbrandy.com
# 2013-...
#


from basic_tests import BaseTestCase
from dasa import utils


class UtilsTestCase(BaseTestCase):

    def test_prettyprint_date(self):
        utils.prettyprint_date(2000, 1, 1)
        utils.prettyprint_date(2000, 12, 32)
        utils.prettyprint_date(2000, None, None)
        utils.prettyprint_date(2000, 'xx', 'yy1')
        utils.prettyprint_date(2000)
        self.assertEqual(utils.prettyprint_date(2000, 11), u'Nov. 2000')
