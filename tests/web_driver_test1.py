import os
import sys
import unittest

from selenium import webdriver
from sauceclient import SauceClient


capabilities = {
    'platform': "Mac OS X 10.9",
    'browserName': "chrome",
    'version': "43",
}

username = os.environ["SAUCE_USERNAME"]
access_key = os.environ["SAUCE_ACCESS_KEY"]


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (username, access_key),
            desired_capabilities=capabilities)

    def tearDown(self):
        self.driver.quit()
        sauce_client = SauceClient(username, access_key)
        status = sys.exc_info() == (None, None, None)
        sauce_client.jobs.update_job(self.driver.session_id, passed=status, name="nose_demo Test1")

    def test_google(self):
        self.driver.get("http://www.google.com")
        self.driver.execute_script("sauce:job-result=passed")
        self.driver.execute_script("sauce:job-name=JD!!!")
        self.assertEqual(self.driver.title, "Google", "Unable to load google page")
        self.driver.execute_script("sauce:context=Logging mah line")
