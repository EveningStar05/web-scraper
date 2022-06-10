import requests
import time
from bs4 import BeautifulSoup # scraper

# Selenium
from selenium import webdriver # web automation
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import csv
import re

# initialize webdriver : Firefox, Chrome, IE and Remote
def launch_browser():

    ser = Service("../chromedriver_linux64/chromedriver")
    op = webdriver.ChromeOptions()
    op.add_argument("--incognito")
    op.add_argument("headless")
    driver = webdriver.Chrome(service=ser, options=op)

    return driver

url = "https://www.imdb.com/title/tt5607976/reviews?ref_=tt_ql_3"
driver = launch_browser()
driver.get(url)

count_page = 0

while True:
    try:
        driver.find_element(By.ID, 'load-more-trigger').click()
        time.sleep(5)
        count_page += 1
        print("page loaded: ", count_page)
    except:
        print("completed loading data...")
        break

get_html = driver.page_source
soup = BeautifulSoup(get_html, "html.parser")

lists_of_content = []

result = soup.find_all("div", class_="lister-item-content")

for x in result:
    content = x.find("div", class_ = re.compile("^text show-more__control")).text
    date = x.find("span", class_="review-date").text
    find_rating = x.find("span", class_ = "rating-other-user-rating")
    if find_rating is not None:
        lists_of_content.append([date, content, find_rating.text.strip()])
    else:
        lists_of_content.append([date, content, None])
    print("retrieving: ", len(lists_of_content), " item.")
    time.sleep(5)

print("Done retrieving data. Total: ", len(lists_of_content))

with open("hdm-review-test.csv", "w") as f:
    headers = ["Date", "Review", "Rating"]
    writer = csv.writer(f)
    writer.writerow(headers)
    
    print("saving....")
    for x in lists_of_content:
        writer.writerow(x)
    print("done!")

f.close()

# TODO: rapihin. less cluttered.



