from splinter import Browser
from bs4 import BeautifulSoup as bs
import re
import pandas as pd


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

def scrape():

    browser = init_browser()
    
    mars_info ={}

    # Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    browser.visit(url)

    browser.is_element_present_by_xpath("/div[3]/div/article/div/section/div/ul/li[1]/div/div/div[2]/a", wait_time =3)
    

    soup = bs(browser.html, "html.parser")


    news_title = soup.find("li", class_="slide").h3.text
    news_p = soup.find("div", class_="article_teaser_body").text

    mars_info["news_title"] = news_title
    mars_info["news_p"] = news_p

    # Featured Image

    url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url_img)

    soup_img = bs(browser.html, "html.parser")

    image = soup_img.find("article", class_="carousel_item")

    route = image['style'][23:-3]
    featured_image_url = f'https://www.jpl.nasa.gov{route}'

    mars_info["featured_image"] = featured_image_url

    # # Mars Weather

    twitter_url ="https://twitter.com/marswxreport?lang=en"

    browser.visit(twitter_url)
    browser.is_element_present_by_xpath("/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div/div[2]/div/div/div/div/article/div/div[2]", wait_time = 1)

    soup_twitter = bs(browser.html, "html.parser")

    mars_weather = soup_twitter.find(text = re.compile("InSight"))

    mars_info["mars_weather"] = mars_weather


    # Mars Facts

    url_facts = "https://space-facts.com/mars/"

    tables = pd.read_html(url_facts)

    mars_facts = tables[0]

    mars_facts_HTML = mars_facts.to_html(header = False, index = False)

    mars_info["mars_facts_HTML"] = mars_facts_HTML


    # # Mars Hemisphers

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemispheres_url)

    soup = bs(browser.html, 'html.parser')

    hemispheres = []
    divs = soup.find_all('div', class_='item')

    for x in range(len(divs)):
        hemispheres.append(divs[x].find('h3').text)

    hemisphere_image_urls =[]


    for x in range(len(hemispheres)):
        
        browser.click_link_by_partial_text(hemispheres[x])
        
        soup_hemispheres = bs(browser.html, "html.parser")
        
        title = soup_hemispheres.title.text.split("|")[0][:-1]
        
        img_url = f'https://astrogeology.usgs.gov{soup_hemispheres.find_all("img", class_ = "wide-image")[0]["src"]}'
        
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        
        browser.back()

    h_i_u = hemisphere_image_urls

    mars_info["h_i_u"] = h_i_u

    browser.quit()

    return (mars_info)
