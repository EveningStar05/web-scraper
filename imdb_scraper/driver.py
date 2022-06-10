from selenium import webdriver
from selenium.webdriver.chrome.service import Service # must use this, .Chrome(..path) is depricated
from selenium.webdriver.chrome.options import Options


def launch_browser():
    ser = Service("../chromedriver_linux64/chromedriver")
    op = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
    op.add_argument("--incognito")
    op.add_argument("headless")
    op.add_argument("user-agent=%s" % user_agent)
    
    driver = webdriver.Chrome(service=ser, options=op)

    return driver
    
