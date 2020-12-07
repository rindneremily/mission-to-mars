# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
#!which chromedriver
# Setup splinter
executable_path = {'/Users/Emily/Documents/Class_data/mars/mission-to-mars/chromedriver': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="/Users/Emily/Documents/Class_data/mars/mission-to-mars/chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data
if __name__ == "__main__":
    print(scrape_all)

from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': '/Users/Emily/Documents/Class_data/mars/mission-to-mars/chromedriver'}
browser = Browser('chrome', **executable_path)

url = 'https://mars.nasa.gov/news/'
browser.visit(url)

browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

html = browser.html
img_soup = soup(html, 'html.parser')

img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()

df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df

df.to_html()

url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

html = browser.html
weather_soup = soup(html, 'html.parser')

weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

hemisphere_image_urls = []

links = browser.find_by_css("a.product-item h3")

for item in range(len(links)):
    hemisphere = {}
    
    browser.find_by_css("a.product-item h3")[item].click()
    
    sample = browser.links.find_by_text("Sample").first
    
    hemisphere["img_url"] = sample["href"]
    
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    hemisphere_image_urls.append(hemisphere)
    
    browser.back()

print(hemisphere_image_urls)

browser.quit()