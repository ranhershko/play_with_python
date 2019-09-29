# coding=utf-8
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from SiteSignupSanity import SiteSignupSanity
import logbook
import random
import os
import time


class SiteGiftSend(SiteSignupSanity):
    def __init__(self):
        self.send_sorry_to = {'wife': 'Nourit', 'mom': 'Chen', 'sister': 'Hodaya'}
        super(SiteGiftSend, self).__init__()
        self.gift_send_logger = logbook.Logger('GiftSendSanity')
        gift_send_msg = 'Start'
        self.gift_send_logger.notice(gift_send_msg)
        self.current_css_selector_button = ''
        self.run_gift_send_sanity()

    def send_amount_to_texboxes(self):
        """Send gift card amount to textbox """
        gift_amount = random.randint(1, 1000)
        how_much_textbox = self.current_browser.find_elements_by_css_selector("input[placeholder='מה הסכום?']")[0]
        how_much_textbox.send_keys(f'{gift_amount}')

    def css_button_n_click(self):
        """get css selector and click"""
        self.current_browser.find_elements_by_css_selector(self.current_css_selector_button)[0].click()

    def run_gift_send_sanity(self):
        """Gift card send - Sanity check run"""
        for_who = self.send_sorry_to[''.join(random.sample(self.send_sorry_to.keys(), 1))]
        for self.current_browser in self.active_browsers.values():
            self.current_browser.implicitly_wait(10)
            self.current_link_2_click = "סופר שובר"
            self.link_n_click()
            gift_to_button = self.current_browser.find_element_by_xpath(
                "//a/span[text()='אני רוצה לתת סופר שובר']/ancestor::a[1]")
            ActionChains(self.current_browser).move_to_element(gift_to_button).click().perform()
            self.send_amount_to_texboxes()
            self.current_browser.find_element_by_css_selector("button[type='submit']").click()
            send_n_receive_textboxes = self.current_browser.find_elements_by_xpath(
                '//input[@data-parsley-group="main"]')
            for textbox in send_n_receive_textboxes:
                who = textbox.get_attribute('data-parsley-required-message')
                if 'למי יגידו תודה' in who:
                    textbox.clear()
                    textbox.send_keys(self.user_info[self.current_browser.capabilities[
                        'browserName']]['user_first_name'])
                elif 'מי הזוכה המאושר' in who:
                    textbox.clear()
                    textbox.send_keys(for_who)
            occasion_type = self.current_browser.find_elements_by_link_text('לאיזה אירוע?')
            ActionChains(self.current_browser).move_to_element(occasion_type[0]).click().perform()
            opt_last_index = len(self.current_browser.find_elements_by_xpath(
                "//li[text()='לאיזה אירוע?']/ancestor::ul[1]/li")) - 1
            chosen = random.randint(1, opt_last_index)
            ActionChains(self.current_browser).move_to_element(self.current_browser.find_elements_by_xpath(
                f"//li[@data-option-array-index='{chosen}']")[0]).click().perform()
            blessing = self.current_browser.find_elements_by_xpath('//textarea')[0]
            placeholder = blessing.get_attribute('placeholder')
            if 'מזל טוב' in placeholder:
                blessing.send_keys(Keys.CONTROL, Keys.HOME)
                blessing.send_keys(f"{for_who} : את חייבת לי\n")
            image_path = os.path.join(os.path.dirname(__file__), "million_balloons.png")
            image_upload_by = self.current_browser.find_element_by_name("fileUpload")
            image_upload_by.send_keys(image_path)
            send_now_checkboxes = self.current_browser.find_element_by_xpath("//label[@class='send-now']")
            if not send_now_checkboxes.is_selected():
                send_now_checkboxes.click()
            all_send_to_by = self.current_browser.find_elements_by_xpath('//span[contains(@class,"btn-text")]')
            for send_to_by in all_send_to_by:
                if send_to_by.text == 'במייל':
                    send_to_by.click()
                    receiver_email = self.current_browser.find_elements_by_xpath(
                        '//input[contains(@placeholder,"כתובת המייל של מקבל/ת המתנה")]')[0]
                    receiver_email.clear()
                    receiver_email.send_keys(f'{for_who}@gmail.com')
                    for send_email_n_submit in "button[type='submit'][class='btn btn-theme btn-save']", \
                                               "button[type='submit'][data-toggle='modal']":
                        self.current_css_selector_button = send_email_n_submit
                        self.css_button_n_click()
            time.sleep(15)
            self.make_screenshot()
            self.current_browser.close()
            if self.current_browser.capabilities['browserName'] == 'chrome':
                kill_chromedriver_cmd = "taskkill /F /IM ChromeDriver.exe"
                print("Return kill cmd value:", os.system(kill_chromedriver_cmd))


