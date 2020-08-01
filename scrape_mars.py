# import needed libraries:

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless = True)
    
    # Visit the NASA news URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    # Scrape page into soup:
    html = browser.html
    soup = bs (html, "html.parser")
    # grab and save the most recent article and its title:
    news_title = soup.find_all("div", class_ = "content_title")[1].a.text
    news_p = soup.find("div", class_ = "article_teaser_body").text

    
    # Visit the JPL Mars URL:
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    # click button to have access to the image
    button = browser.find_by_id('full_image')
    button.click()
    time.sleep(1)
    # Scrape page into soup and print it:
    html = browser.html
    soup = bs (html, "html.parser")
    # grab and save image url for the current Featured Mars:
    image_url = soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = "https://jpl.nasa.gov"+image_url

    # Visit the Mars Weather twitter URL
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)
    # Scrape page into soup:
    html = browser.html
    soup = bs (html, "html.parser")
    # grab and save the most recent twit about mars weather
    mars_weather_all = soup.find_all('span')
    for i in range(len(mars_weather_all)):
        if ("InSight" in mars_weather_all[i].text):
            mars_weather = mars_weather_all[i].text
            break    
    
    # Visit the Mars Facts URL
    url = "https://space-facts.com/mars/"
    # save table
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ["Parameter","Value"]
    # convert dataframe to html file usig pandas
    html_table = df.to_html()
    
    #  Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    mars_hemis = []
    for i in range (4):
        time.sleep(1)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial_url = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial_url
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back() 
        
    # Save all scraped data in a dictionary
    mars_data = {}
    mars_data = {"news_title": news_title,
                 "news_p": news_p,
                 "featured_image_url": featured_image_url,
                 "mars_weather": mars_weather,
                 "html_table": html_table,
                 "mars_hemis": mars_hemis}
 
    return mars_data

