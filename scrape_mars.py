from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import time
import pandas as pd
import pymongo
import datetime as dt

def scrape_all():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    article = soup.find('div',class_="list_text")

    try:
        title = article.find('div',class_='content_title').text.strip()
    except: 
        title = '[No information returned. Click the button again.]'
    try:
        para = article.find('div',class_='article_teaser_body').text.strip()
    except:
        para = '[No information returned.  Click the button again.]'

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_id('full_image')

    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

    featured_image_url = soup.article.a['data-fancybox-href']
    featured_image_url = (f'https://www.jpl.nasa.gov{featured_image_url}')
    descrip =soup.h1.text.strip()

    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    tables = pd.read_html(url)

    df = tables[0]
    df.columns = ['', 'Mars']
    df = df.set_index('')

    mars_facts= df.to_html(classes='table')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Click the link for large image, find title and link, add try and except, store in dict format, append to dict
    hemisphere_image_urls_dict = []
    for i in range(4):
        browser.find_by_css("a.product-item h3")[i].click()
        hemi_soup = BeautifulSoup(browser.html, "html.parser")

        try:
            title_elem = hemi_soup.find("h2", class_="title").get_text()
            sample_elem = hemi_soup.find("a", text="Sample").get("href")

        except AttributeError:
            title_elem = None
            sample_elem = None

        hemispheres = {
            "title": title_elem,
            "img_url": sample_elem
        }

        # Append hemisphere info
        hemisphere_image_urls_dict.append(hemispheres)

        # Finally, we navigate backwards
        browser.back()

    browser.quit()

    data = {
        'news_title':title,
        'news_paragraph':para,
        'featured_image': featured_image_url,
        'featured_image_description':descrip,
        'hemisphere_image_urls': hemisphere_image_urls_dict,
        'facts':mars_facts,
        'last_modified':dt.datetime.now()
    }

    return(data)