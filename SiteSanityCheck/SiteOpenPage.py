import logbook
import sys
import os
import random
import string
from datetime import datetime
from shutil import which
from collections import defaultdict
from selenium import webdriver
from pathlib import Path
from selenium.common.exceptions import TimeoutException
from urllib3.exceptions import MaxRetryError


class SiteOpenPage:

    def __init__(self):
        self.base_url = ""
        self.base_url_file = "site_url.txt"
        # self.browsers_drv = {'firefox': webdriver.Firefox, 'chrome': webdriver.Chrome}
        self.browsers_drv = {'chrome': webdriver.Chrome}
        self.drivers_files = {'chrome': 'chromedriver.exe'}
        # self.drivers_files = {'firefox': 'geckodriver.exe', 'chrome': 'chromedriver.exe'}
        self.active_browsers = defaultdict(dict)
        self.current_browser = ""
        self.first_name = ['Vadim', 'Mona', 'Angela', 'Anna', 'Alex', 'Danniela', 'Meital']
        self.user_info = self.get_user_info()
        self.init_logging('site-sanity.log')
        self.open_page_logger = logbook.Logger('OpenPageSanity')
        open_page_msg = 'Start'
        self.open_page_logger.notice(open_page_msg)
        self.generate_browser()

    @staticmethod
    def create_dir_if_not_exists(directory):
        """Create logs & results dir """
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def get_user_info(self):
        """Create random user or get from file after signup"""
        user_info = defaultdict(dict)
        for browser_type in self.browsers_drv.keys():
            user_info_filename = f"{browser_type}_user_info.txt"
            user_info_file = Path(user_info_filename)
            if not user_info_file.exists():
                user_info[browser_type] = self.get_random_user(random.sample(self.first_name, 1))
                with open(user_info_filename, "a+", encoding='utf-8') as append_file:
                    for name, name_value in user_info[browser_type].items():
                        append_file.write(name + ' : ' + name_value + '\n')
            else:
                with open(user_info_filename, "r") as readfile:
                    lines = readfile.read().splitlines()
                    first_name = lines[-3].split(':')[1].strip()
                    email = lines[-2].split(':')[1].strip()
                    user_pass = lines[-1].split(':')[1].strip()
                    user_info[browser_type] = {
                        'user_first_name': first_name,
                        'user_email': email,
                        'user_pass': user_pass
                    }
        return user_info

    @staticmethod
    def random_str(string_length=10, is_pass=None):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        if is_pass:
            return (''.join([random.choice(letters) for _ in range(string_length)]) + str(random.randint(1, 10))) \
                .capitalize()
        else:
            return ''.join([random.choice(letters) for _ in range(string_length)])

    def get_random_user(self, first_name):
        """Get random user name from first_name list and
        return demo user info """
        return {
            'user_first_name': random.choice(first_name),
            'user_email': self.random_str(6) + '@gmail.com',
            'user_pass': self.random_str(is_pass=True)
        }

    @staticmethod
    def init_logging(log_filename: str = None):
        """Log init method using logbook - logging system for Python that replaces the standard library's logging """
        level = 'NOTICE'

        if not log_filename:
            logbook.StreamHandler(sys.stdout, level=level).push_application()
        else:
            logbook.TimedRotatingFileHandler(log_filename, level=level).push_application()
        msg = 'Sanity Logging initialized, level: {}, mode: {}' \
            .format(level, 'stdout mode' if not log_filename else 'file mode: ' + log_filename)
        sanity_site_log = logbook.Logger(msg)
        sanity_site_log.notice(msg)

    @staticmethod
    def is_tool_exists(name):
        """Check if browser webdriver is on PATH and marked as executable."""
        return which(name) is not None

    def read_url_file(self):
        """Get site url from file """
        try:
            with open(self.base_url_file, "r") as readfile:
                lines = readfile.read().splitlines()
                self.base_url = lines[0].strip()
        except FileNotFoundError as fnfe:
            file_not_found_msg = f"ERROR: Could not find the site url file, Create site_url.txt file with the site " \
                                 f"url for sanity\n. "f"{fnfe}"
            self.open_page_logger.error(file_not_found_msg)
            print(file_not_found_msg)
            exit(1)
        except:
            print(f"Failed to open site_url.txt")

    def generate_browser(self):
        """Use browser webdriver to open connection to the site """
        self.read_url_file()
        timeout_num = 0
        browsers_4_del = []
        for browser_type in self.browsers_drv.keys():
            if self.is_tool_exists(self.drivers_files[browser_type]):
                log_name = datetime.now().strftime(f'{browser_type}_%H_%M_%d_%m_%Y.log')
                log_path = f"{self.create_dir_if_not_exists('logs')}\\{log_name}"
                self.current_browser = self.browsers_drv[browser_type](service_log_path=log_path)
                self.current_browser.set_page_load_timeout(30)
                get_timeout_exception = True
                while get_timeout_exception:
                    try:
                        self.current_browser.delete_all_cookies()
                        self.current_browser.get(self.base_url)
                        self.current_browser.maximize_window()
                    except ConnectionError as ce:
                        server_network_msg = f"ERROR: Could not find the server, Check your network connection. {ce}"
                        self.open_page_logger.error(server_network_msg)
                        if timeout_num == 5:
                            browsers_4_del.append(browser_type)
                    except TimeoutException as te:
                        timeout_msg = f"Timeout problem!: {te}"
                        self.open_page_logger.error(timeout_msg)
                        self.current_browser.quit()
                        timeout_num += 1
                        if timeout_num == 5:
                            browsers_4_del.append(browser_type)
                    except MaxRetryError as mre:
                        max_retry_msg = f"Max retries exceeded: {mre}"
                        self.open_page_logger.error(max_retry_msg)
                        exit(100)
                    except:
                        all_other_errors = f"Something else happened with opening the site url: "
                        self.open_page_logger.error(all_other_errors)
                    finally:
                        if self.current_browser is not None:
                            self.active_browsers[browser_type] = self.current_browser
                            get_timeout_exception = False

            else:
                print(f"{browser_type} driver: {self.drivers_files[browser_type]} isn't in OS path or isn't executable")
        for browse_type in browsers_4_del:
            del self.browsers_drv[browse_type]
