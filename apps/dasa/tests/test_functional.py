#
# http://jeanphix.me/2012/01/20/django-real-world-functional-testing/

# from django.test import LiveServerTestCase
#
# from selenium.webdriver.firefox.webdriver import WebDriver
#
# from selenium.webdriver.support.ui import WebDriverWait
#
#
# class BaseLiveTest(LiveServerTestCase):
#    @classmethod
#    def setUpClass(cls):
#        cls.selenium = WebDriver()
#        super(BaseLiveTest, cls).setUpClass()
#
#    @classmethod
#    def tearDownClass(cls):
#        super(BaseLiveTest, cls).tearDownClass()
#        cls.selenium.quit()
#
#
# class LiveHomeTest(BaseLiveTest):
#    def test_post_submission(self):
#        self.selenium.get(self.live_server_url)
#        message = self.selenium.find_element_by_name("message")
#        message.send_keys('my message')
#        self.selenium.find_element_by_name("author").send_keys('jeanphix')
#        self.selenium.find_element_by_xpath('//input[@value="Send"]').click()
#        WebDriverWait(self.selenium, 10).until(
#            lambda x: self.selenium.find_element_by_css_selector('ul li'))
#        self.assertEqual(initial_posts_count + 1, Post.objects.count())
