import time
import threading
from selenium import webdriver

def skipAdFunction():
    threading.Timer(5,skipAdFunction).start()
    if(skipAd.is_enabled() or skipAd.is_displayed()):
        skipAd.click()

browser = webdriver.Chrome()
browser.get('https://www.youtube.com')

textbox = browser.find_element_by_id('search')
textbox.send_keys('No man no cry - Jimmy Sax (live)')
button = browser.find_element_by_id('search-icon-legacy')
button.click()
browser.implicitly_wait(10)
play_it_by = browser.find_element_by_link_text('No man no cry - Jimmy Sax (live)')
browser.implicitly_wait(10)
play_it_by.click()
time.sleep(360)
browser.close()
