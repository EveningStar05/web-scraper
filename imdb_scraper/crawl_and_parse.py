from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup

from driver import launch_browser
from scraper import scrap_review, scrap_show_info, save

import time

test_url_series = ["https://www.imdb.com/title/tt5607976/", "https://www.imdb.com/title/tt0925266/", "https://www.imdb.com/title/tt1520211/", "https://www.imdb.com/title/tt6704972/", "https://www.imdb.com/title/tt14460684/", "https://www.imdb.com/title/tt2442560/"]
driver = launch_browser()
driver.get(test_url_series[0])

def driver_wait():
    return WebDriverWait(driver, 10)

def click_link(locator, elem): # click the link to view the number of episode
    try:
        wait = driver_wait()
        element = wait.until(EC.element_to_be_clickable((locator, elem)))
    finally:
        element.click()

def check_element(locator, elem):
    try:
        wait = driver_wait()
        get_element = wait.until(EC.presence_of_element_located((locator, elem)))
        if get_element:
            return True
    except:
        return False

def findElement(locator, elem): # find one
    try:
        driver.implicitly_wait(20)
        get_element = driver.find_element(locator, elem)
        return get_element
    except:
        return False

def findElements(locator, elem): # find all
    try:
        driver.implicitly_wait(20)
        get_elements = driver.find_elements(locator, elem)
        return get_elements
    except:
        return False

def parser(url):
    driver.get(url)
    get_page = driver.page_source
    parse = BeautifulSoup(get_page, "html.parser")
    return parse

def sleep():
    for x in range(10, 0, -1):
        print(f"sleep: {x}", end="\r", flush=True)
        time.sleep(2)

def get_review():
    try: # if the page has "User review" link button
        find_review = findElement(By.CSS_SELECTOR, "div[data-testid='reviews-header'] > a:nth-child(1)").get_attribute("href")
        print("review link page: ", get_review)
        if check_element(By.ID, "load-more-trigger"): # click load more button, if exist
            while findElement(By.ID, "load-more-trigger").is_displayed():
                try:
                    click_link(By.ID, "load-more-trigger")
                    sleep()
                except:
                    break
        get_page = parser(find_review)
        return scrap_review(get_page) # scrap the "User review" page
    except: # if review does not exist then continue the iteration until it's finish.
        print("There is no review!")

# TODO: if review does not exist, set it to empty string/NaN atleast there should be show information.

def navigation():
    click_link(By.CSS_SELECTOR, "a[aria-label='View episode guide']")
    get_seasons = [x for season in findElements(By.ID, "bySeason") for x in season.text.split()] # number of seasons in the show
    print("Getting number of seasons...")
    # traverse through each season
    for num_season in get_seasons:
        # select num_season
        select_seasons = Select(findElement(By.ID, "bySeason")) 
        print("Selecting number of seasons...")
        sleep()
        select_seasons.select_by_visible_text(num_season)

        print("Selected number of season!")
        # get all the episode links
        find_all_episodes = [episodes.get_attribute("href") for episodes in findElements(By.CSS_SELECTOR, "div[class='image'] > a")] # find all link of episodes under the div tag
        count_eps = 0
        print("season: ", num_season)
        # traverse through each episode and do the following:
        # go to the first episode, click user reviews, repeat. 
        for num_episode in find_all_episodes:
            print("Accessing episode links...")
            count_eps += 1
            episode_info = parser(num_episode)
            sleep()
            print("Episode num: ", count_eps)
            scrap_info = scrap_show_info(episode_info) # get the episode info
            print("check if 'User review' exist...")
            review = get_review()

            save(review, scrap_info)
            if count_eps == len(find_all_episodes):
                driver.back()
                click_link(By.LINK_TEXT, "All episodes")
    print("completed...")
        
navigation()
