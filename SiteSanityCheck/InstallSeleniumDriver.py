import requests

firefox_url = 'https://github.com/mozilla/geckodriver/releases/download/v0.25.0/geckodriver-v0.25.0-win64.zip'
chrome_url = 'https://chromedriver.storage.googleapis.com/78.0.3904.11/chromedriver_win32.zip'
for file_url in chrome_url, firefox_url:
    myfile = requests.get(file_url)
    driver_filename = ''
    with open(driver_filename, 'wb') as f:
        # Getting url content as a driver file in
        # binary format
        # write the contents of the response (r.content)
        # to a new file in binary mode.
        f.write(myfile.content)

#
# open('c:/users/LikeGeeks/downloads/PythonImage.png', 'wb').write(myfile.content)