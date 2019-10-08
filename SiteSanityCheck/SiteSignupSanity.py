# coding=utf-8
import time
import logbook
import random
from pathlib import Path
from SiteOpenPage import SiteOpenPage
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class SiteSignupSanity(SiteOpenPage):

    def __init__(self):
        self.btn_css_span_click_on = {'signup_btn': "span[class='text-btn']"}
        self.account_info = {'account_info': 'החשבון שלי'}
        if self.__class__.__name__ == SiteSignupSanity.__name__ or not Path('chrome_user_info.txt').exists():
            self.signup = True
            self.move_user_for_new_signup()
        else:
            self.signup = False
        super(SiteSignupSanity, self).__init__()
        self.signup_logger = logbook.Logger('SignupSanity')
        signup_msg = 'Start'
        self.signup_logger.notice(signup_msg)
        self.current_search_category = ""
        self.current_link_2_click = ""
        self.run_signup_login_sanity()

    def move_user_for_new_signup(self):
        """backup and delete old user before signup """
        for browser_type in 'firefox', 'chrome':
            user_info_filename = f"{browser_type}_user_info.txt"
            user_info_file = Path(user_info_filename)
            if user_info_file.exists():
                user_info_file.replace(user_info_file.stem + '.' + time.strftime('%Y-%m-%d-%H-%M') + '.txt')

    def find_n_click_on(self, browse, css_elm_str, button_name_elm):
        """Button click using css to enter the signup page"""
        elm_button = dict()
        elm_button[button_name_elm] = browse.find_element_by_css_selector(css_elm_str)
        if elm_button[button_name_elm].text != 'לכניסה':
            elm_button[button_name_elm].click()

    def send_keys_to_texboxes_on(self, search_engine):
        """Fill user info in signup form """
        user_reg_text_boxes = search_engine.find_elements_by_css_selector("input[class='ember-view ember-text-field']")
        if search_engine.capabilities['browserName'] == 'chrome':
            user_info = self.user_info['chrome']
        elif search_engine.capabilities['browserName'] == 'firefox':
            user_info = self.user_info['firefox']
        try:
            for textbox in user_reg_text_boxes:
                placeholder = textbox.get_attribute('placeholder')
                if placeholder == 'שם פרטי':
                    textbox.send_keys(user_info['user_first_name'])
                elif placeholder == 'מייל':
                    textbox.send_keys(user_info['user_email'])
                elif 'סיסמה' in placeholder:
                    textbox.send_keys(user_info['user_pass'])
        except:
            dont_know_msg = "Didn't work on that yet ..."
            self.signup_logger.error(dont_know_msg)

    def checkboxes_check_or_not(self, search_engine):
        """
        Clicked checkboxes for confirmation
        :param search_engine: browser driver
        """
        user_reg_checkboxes = search_engine.find_elements_by_xpath("//i")
        for checkbox in user_reg_checkboxes:
            if checkbox.find_element_by_xpath("./..").text == 'אני מסכים לתנאי התקנון ולמדיניות הפרטיות':
                if 'checked' not in checkbox.get_attribute("class"):
                    ActionChains(search_engine).move_to_element(checkbox).click().perform()
            elif checkbox.find_element_by_xpath("./..").text == 'אשמח לקבל עדכונים ופרסומים על מבצעים ומתנות חדשות':
                if 'checked' in checkbox.get_attribute("class"):
                    ActionChains(search_engine).move_to_element(checkbox).click().perform()

    def make_screenshot(self):
        """Make result screenshot """
        screenshot_filename = f"{self.create_dir_if_not_exists('results')}\\{self.current_browser.capabilities['browserName']}_{self.__class__.__name__}.png"
        self.current_browser.save_screenshot(screenshot_filename)

    def drop_n_choose(self):
        """Click dropdown menu and choose """
        # search_type_link = self.current_browser.find_elements_by_link_text(self.current_search_category)
        WebDriverWait(self.current_browser, 20).until(ec.element_to_be_clickable(
            (By.LINK_TEXT, self.current_search_category)))
        search_type_link = self.current_browser.find_elements_by_link_text(self.current_search_category)
        ActionChains(self.current_browser).move_to_element(search_type_link[0]).click(search_type_link[0]).perform()
        opt_last_index = len(self.current_browser.find_elements_by_xpath(
            f"//li[text()=\'{self.current_search_category}\']/ancestor::ul[1]/li")) - 1
        chosen = random.randint(1, opt_last_index)
        ActionChains(self.current_browser).move_to_element(self.current_browser.find_elements_by_xpath(f"//li[@data-option-array-index='{chosen}']")[0]).click().perform()

    def link_n_click(self):
        """Find link locator and click"""
        link_search = self.current_browser.find_element_by_link_text(self.current_link_2_click)
        WebDriverWait(self.current_browser, 30).until(ec.element_to_be_clickable((
            By.LINK_TEXT, self.current_link_2_click)))
        self.current_browser.execute_script("arguments[0].click();", link_search)

    def run_signup_login_sanity(self):
        """Full signup Sanity check run"""
        for current_browser in self.active_browsers.values():
            self.current_browser = current_browser
            self.current_browser.find_elements_by_xpath("//span[text()='הרשמה']/ancestor::a[1]")[0].click()
            if self.signup:
                for btn_str, span_css_str in self.btn_css_span_click_on.items():
                    self.find_n_click_on(self.current_browser, span_css_str, btn_str)
            self.send_keys_to_texboxes_on(self.current_browser)
            if self.signup:
                self.checkboxes_check_or_not(self.current_browser)
            self.current_browser.find_element_by_css_selector("button[type='submit']").click()
            self.current_browser.implicitly_wait(10)
            if self.signup and self.__class__.__name__ == SiteSignupSanity.__name__:
                account_info = self.current_browser.find_elements_by_link_text(self.account_info['account_info'])
                ActionChains(self.current_browser).move_to_element(account_info[0]).click().perform()
                time.sleep(15)
                self.make_screenshot()
                self.current_browser.close()
                # if self.current_browser.capabilities['browserName'] == 'chrome':
                #     kill_chromedriver_cmd = "taskkill /F /IM ChromeDriver.exe"
                #     print("Return kill cmd value:", os.system(kill_chromedriver_cmd))
