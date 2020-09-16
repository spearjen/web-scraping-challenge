# import necessary libraries
from flask import Flask, render_template

# create instance of Flask app
app = Flask(__name__)

@app.route("/scrape")

#call the dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd
master_mars_dict={}
from flask import Flask, render_template
import pymongo

def scrape-mars():
    #connect to mongodb
    conn='mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db=client.marsDB

    #executable path for chromedriver/splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #browser visit
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #soup object
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    articles = soup.find_all('div',class_='list_text')

    #blank lists and dict
    news_dict=[]
    title_list=[]
    para_list=[]

    #loop through page and get titles and paragraphs
    for article in articles:
        title = article.find('a').text.strip()
        title_list.append(title)
        para = article.find('div',class_='article_teaser_body').text.strip()
        para_list.append(para)
        news_pairs = {
        "news_title": title,
        "news_para": para
        }
        #append hemisphere object to list
        news_dict.append(news_pairs)

    #create marsDB catalog, news
    db.mars_news.insert_many(news_dict)

    #browser visit
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #splinter click to go to full image
    browser.click_link_by_id('full_image')

    #soup object
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    #get featured image and description
    featured_image_url = soup.article.a['data-fancybox-href']
    featured_image_url = (f'https://www.jpl.nasa.gov{featured_image_url}')
    descrip =soup.h1.text.strip()

    #create featured image dict
    featured_image_dict=[]
    featured_image_dict = [{
        "featured_image_url": featured_image_url,
        "description": descrip
        }]

    #create marsDB catalog, featimg
    db.mars_featimg.insert_many(featured_image_dict)

    #browser visit
    url = 'https://space-facts.com/mars/'

    #html to pandas table
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['info_type', 'mars_fact']

    #create dictionary from df
    facts_dict = df.to_dict('records')
    db.mars_facts.insert_many(facts_dict)

    #browser visit
    url = ("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    browser.visit(url)

    #click the link, find anchor, return the href
    hemisphere_image_urls_dict = []
    for i in range(4):

        #find the elements on each loop
        browser.find_by_css("a.product-item h3")[i].click()
        hemi_soup = BeautifulSoup(browser.html, "html.parser")

        #add try/except for error handling
        try:
            title_elem = hemi_soup.find("h2", class_="title").get_text()
            sample_elem = hemi_soup.find("a", text="Sample").get("href")

        except AttributeError:

    # error= return none
            title_elem = None
            sample_elem = None

        hemispheres = {
            "title": title_elem,
            "img_url": sample_elem
        }

        #append hemisphere to list
        hemisphere_image_urls_dict.append(hemispheres)

        #navigate backwards
        browser.back()

    db.mars_hemi.insert_many(hemisphere_image_urls_dict)

if __name__ == "__main__":
    app.run(debug=True)
