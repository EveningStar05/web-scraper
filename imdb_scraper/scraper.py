import csv
import time
import re 

def scrap_show_info(page):
    body = page.find_all("div", class_="sc-5ca7bdd8-1 eXWgfK ipc-page-grid__item ipc-page-grid__item--span-2")
    avg_rating = page.find("span", class_="sc-7ab21ed2-1 jGRxWM").text # TODO: remove this also
    episode_num = page.find("div", attrs={"data-testid": "hero-subnav-bar-season-episode-numbers-section-xs"}).text.split(".")
    
    show_content = []
    for x in body:
        # x.select("li[data-testid='title-techspec_runtime'] > div")
        runtime = x.find("li", attrs={"data-testid": "title-techspec_runtime"}).text.split("Runtime")[1]
        # x.select("li[data-testid='title-details-releasedate'] > div")
        date = x.find("li", attrs={"data-testid": "title-details-releasedate"}).text.split("Release date")[1]
        # x.select("li[data-testid='title-details-origin'] > div")
        # country = x.find("li", attrs={"data-testid": "title-details-origin"}).text.split("Country of origin")[1]
        director = x.find("div", class_="ipc-metadata-list-item__content-container").text
        show_content.append([episode_num[0], episode_num[1], avg_rating, runtime, date, director])
    return show_content[0]

def scrap_review(page):
    get_title = page.find("h4").text.lower().replace(" ", "-")
    review_container = page.find_all("div", class_=re.compile("^lister-item mode-detail"))
    get_content = []
    
    for content in review_container:
        review_content = content.find("div", class_ = re.compile("^text show-more__control")).text #review-container
        rating = content.find("span", class_ = "rating-other-user-rating") # if the element has no rating, set it to 0
        user_name = content.find("span", class_="display-name-link").text
        date = content.find('span', class_="review-date").text
        votes = re.findall("[0-9]+", content.find("div", class_= re.compile("^actions text-muted")).text) # 0: number of votes, 1: total votes

        # TODO:set the rating to None is there is no rating
        if rating is not None:
            get_content.append([user_name, date, rating.text.strip(), review_content, votes[0], votes[1]])
        else:
            get_content.append([user_name, date, None, review_content, votes[0], votes[1]])
    return get_title, get_content

def save(review_content, show_info):
    file_name, review = review_content
    header_exist = False
    with open("{name}.csv".format(name=file_name), "a+") as f:
        if not header_exist:
            headers_review = ["user_name", "review_date", "rating", "review", "helpful_votes", "total_helpful_votes", "season", "episode_number", "avg_rating", "run_time", "release_date", "director"]
            header_exist = True
            write = csv.writer(f)
            write.writerow(headers_review)

        for x in review:
            for i in show_info:
                x.append(i)
            write.writerow(x)