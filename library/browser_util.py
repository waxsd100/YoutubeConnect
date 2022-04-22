from selenium import webdriver
# from selenium.webdriver.chrome import service as cs
from selenium.webdriver.firefox import service as fs


def get_web_driver():
    firefox_option = webdriver.FirefoxOptions()
    firefox_option.add_argument("--window-size=500,800")
    firefox_option.add_argument("--width=500")
    firefox_option.add_argument("--height=800")
    firefox_servie = fs.Service(executable_path="bin/geckodriver.exe")

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--disable-gpu')
    # # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_servie = cs.Service(executable_path="bin/chromedriver.exe")

    return webdriver.Firefox(service=firefox_servie, options=firefox_option)
    # return webdriver.Chrome(service=chrome_servie, options=chrome_options)


def open_browser(driver, url):
    driver.get(url)
    driver.implicitly_wait(1)
    return driver
