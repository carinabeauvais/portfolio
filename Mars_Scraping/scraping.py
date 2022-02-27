# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# initialize browser, create data dictionary and end webdriver and return scraped data
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # set news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary. This runs functions we created. Add date it was run.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # end automated browsing session
    # Stop webdriver and return data
    browser.quit()
    return data

#add argument to function, browser tells python we are using the browser variable we defined outside of the function
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page. search elements with div tag and list_text attribute, add 1 sec delay
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up HTML parser, assign varable to look for div tag and its descendent.
    # . selects classes so div.list_text pinpoints the div tag with class of list_text.
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # add try except clause to address attribute errors before beginning the scrape
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    # add a return statement
    return news_title, news_p

# ### Featured Images

# define statement
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

       
    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

### Mars Facts

# define function
def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        # create new dataframe from HTML table. Pandas read_html() searches and returns list of tables.
        # Specifying index of 0, we are telling Pandas to pull only first table or first item in the list and turns into df.
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
      return None

    
    # assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    # add .to_html() to convert df back to html ready code, add bootstrap
    return df.to_html()
    
# tell Flask script is complete and ready. print statement prints results to terminal after executing the code
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())