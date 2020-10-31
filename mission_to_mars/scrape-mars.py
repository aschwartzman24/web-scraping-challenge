# imports
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    
    # --- Visit Mars News site ---
    browser.visit('https://mars.nasa.gov/news/')


    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    

    # find container holding news title and paragraph
    article_list = soup.find("ul",class_="item_list")
    # search for title
    news_title = article_list.find("div",class_="content_title").text
    # search for paragraph
    news_p = article_list.find("div",class_="article_teaser_body").text

    
    # Open browser to JPL Featured Image
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    # Click through to find full image
    browser.click_link_by_partial_text('FULL IMAGE')

    # Click again for full large image
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    
    # Scrape JPL page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Search for image source
    results = soup.find_all('figure', class_='lede')
    relative_img_path = results[0].a['href']
    featured_img = 'https://www.jpl.nasa.gov' + relative_img_path
    
    # visit space facts website and scrape facts table
    url = 'https://space-facts.com/mars/'
    mars_facts_table = pd.read_html(url)[0]
    mars_facts_table = mars_facts_table.rename(columns={0:'Mars', 1:'Value'})
    mars_facts_table = mars_facts_table.set_index('Mars', drop=True)
    
    # Converting table to HTML
      mars_facts_table = [mars_facts_table.to_html(classes='data table table-borderless', index=False, header=False, border=0)]

    # Opening browser to USGS site
    browser.visit= ("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")


    html = browser.html
    soup = bs(html,'html.parser')
    
    
    mars_hemisphere = []

    # hempisheres variable holds title and img url
    hemispheres = products.find_all(class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find(class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
        
        
      # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_img,
        "weather": mars_weather,
        "mars_facts": mars_facts_table,
        "hemispheres": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
