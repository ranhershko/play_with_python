# coding=utf-8
from SiteSignupSanity import SiteSignupSanity
import logbook
import time
import os


class SiteHomeSearch(SiteSignupSanity):
    def __init__(self):
        self.SEARCH = {'AMOUNT': 'סכום', 'AREA': 'אזור', 'CATEGORY': "קטגוריה"}
        self.FIND_ME_A_GIFT = 'תמצאו לי מתנה'
        super(SiteHomeSearch, self).__init__()
        self.home_search_logger = logbook.Logger('HomeSearchSanity')
        home_search_msg = 'Start'
        self.signup_logger.notice(home_search_msg)
        self.run_home_search_sanity()

    def drops_n_chooses(self):
        """Multi Click dropdown menu and choose """
        for category in self.SEARCH.keys():
            self.current_search_category = self.SEARCH[category]
            self.drop_n_choose()

    def run_home_search_sanity(self):
        """Home site search Sanity check run"""
        for self.current_browser in self.active_browsers.values():
            self.drops_n_chooses()
            find_gift_by = self.current_browser.find_element_by_partial_link_text(self.FIND_ME_A_GIFT)
            find_gift_by.click()
            time.sleep(15)
            self.make_screenshot()
            self.current_browser.close()
            # if self.current_browser.capabilities['browserName'] == 'chrome':
            #     kill_chromedriver_cmd = "taskkill /F /IM ChromeDriver.exe"
            #     print("Return kill cmd value:", os.system(kill_chromedriver_cmd))


