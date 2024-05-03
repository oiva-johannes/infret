from time import sleep
import os.path
import requests
import re
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from dateutil import parser
from utils.utils import read_data, write_data, lemmatize_documents, read_lemmatized_documents
from utils.pil import resize_image
from utils.dates_delete import filter_dates
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from PIL import Image
from search_methods.semantic_search import convert_to_tagged, load_tagged, create_vectors


## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Set path to chrome/chromedriver as per your configuration
homedir = os.path.expanduser("~")
chrome_options.binary_location = f"{homedir}/infret/chrome-linux64/chrome"
webdriver_service = Service(f"{homedir}/infret/chromedriver")


def ScrapeYle(articles: list[pd.DataFrame]):

    old_links = []
    if articles:
        old_links = articles[0].to_dict('list')['href']

    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    driver.get("https://yle.fi")
    sleep(2)
    print("Waiting for few seconds...")
    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Set how many pixels you want to scroll each step
    step_size = 300

    # Gradually scroll down the page
    for y in range(0, total_height, step_size):
        driver.execute_script(f"window.scrollTo(0, {y});")
        sleep(0.1)  # Adjust sleep time as needed for the page to render.

    # Scroll to the very bottom to ensure the entire page is loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    # Now that the page is loaded, including dynamic content, get the page source
    html = driver.page_source
    driver.quit()

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    news_main = soup.main
    headlines = []

    for child in news_main:
        img_tag = child.img
        if img_tag and 'src' in img_tag.attrs:
            image_src = img_tag['src']
            headline = child.find('a', class_="underlay-link")
            headlines.append((headline,image_src))

    #headlines = soup.find_all('a', class_="underlay-link") #Find all the headers 

    already_seen = set()
    
    for index, (headline, image_src) in enumerate(headlines):
        if headline.text not in already_seen:
            already_seen.add(headline.text)
            
            href = re.findall('href.*\">', str(headline))[0]
            if "https://areena.yle.fi" in href:
                print(None, "YLE: wrong type")
                continue
            
            if "https://yle.fi" not in href:
                href = "https://yle.fi"+href[6:-2]
            else:
                href = href[6:-2]

            if href in old_links:
                print(None, "YLE: old href")
                continue
            
            source_article = requests.get(href)
            source_article.raise_for_status()
            bsoup = BeautifulSoup(source_article.text, "html.parser")

            content = bsoup.find('section', class_="yle__article__content")
            if content == None or content.text == None or content.text == "" or content.text == [] or content == "":
                print(None, "YLE: content")  # debug print
                continue

            print("YLE:", href) # debug print

            rege = re.compile('.*yle__article__paragraph')
            p = bsoup.find(class_=rege)
            if p == None:
                paragraph = ""
            else:
                paragraph = p.text

            time = bsoup.find('time', class_="aw-lsqctp jPSFYl yle__article__date--published")
            date = re.findall('datetime.*">', str(time))
            if len(date) != 0:
                date = date[0][10:-2]
                dt_object = parser.parse(date)
                fin_zone = dt_object.astimezone(ZoneInfo("Europe/Helsinki"))
                date = fin_zone.strftime('%d.%m.%Y')
            else:
                fin_zone = datetime.now(ZoneInfo("Europe/Helsinki"))
                date = fin_zone.strftime('%d.%m.%Y')
            
            

            text = content.text
            popularity = index+1
            provider = "YLE"
            header = headline.text

        response = requests.get(image_src)

        if response.status_code == 200:
            # The content of the response contains the image binary data
            req_image = response.content

            # Specify the location and name of the file to save the image
            
            imagepath = f'static/images/{href.replace("/", "_")}.png'

            # Open a file in binary write mode and write the image data
            with open(imagepath, 'wb') as f:
                f.write(req_image)
            resize_image(imagepath, imagepath, 200, 125)
            print("Image done")


            df = pd.DataFrame({
                "popularity": popularity,
                "header": header,
                "href": href,
                "date": date,
                "provider": provider,
                "paragraph": paragraph,
                "imagepath": imagepath,
                "text": text,}, index=[len(articles)+1])
            
            articles.append(df)

def ScrapeIS(articles: list[pd.DataFrame]):

    old_links = []
    if articles:
        old_links = articles[0].to_dict('list')['href']

    # Get page
    # Choose Chrome driver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    driver.get("https://www.is.fi")

    # Extract description from page and print
    iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//iframe[@title="SP Consent Message"]')))
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[@title="OK"]'))).click()
    sleep(2)
    print("Waiting for few seconds...")
    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Set how many pixels you want to scroll each step
    step_size = 300

    # Gradually scroll down the page
    for y in range(0, total_height, step_size):
        driver.execute_script(f"window.scrollTo(0, {y});")
        sleep(0.1)  # Adjust sleep time as needed for the page to render.

    # Scroll to the very bottom to ensure the entire page is loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Now that the page is loaded, including dynamic content, get the page source
    html = driver.page_source
    driver.quit()

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    headlines = []
    # Now you can use BeautifulSoup as before to parse the page
    sections = soup.find('section', class_="w-full max-w-main lg:w-main")
    for section in sections:
        is_articles = section.find_all('article')
        for is_article in is_articles:
            img_tag = is_article.img
            if img_tag and 'src' in img_tag.attrs:
                image_src = img_tag['src']
                headline = is_article.find('a', class_='block')
                headlines.append((headline,image_src))

    #print(headlines[:2])
    #print(len(headlines))
    #headlines = section.find_all('a', class_='block')

    already_seen = set()

    for index, (headline,image_src) in enumerate(headlines):
        if headline == None:
            continue
        if headline.text not in already_seen:
            already_seen.add(headline.text)
        else:
            print(None, "IS: seen already")
            continue

        href_ending = headline.get('href')
        if "http" in href_ending or "mainos" in href_ending:
            print(None, "IS: wrong type")
            continue
        href = "https://www.is.fi"+href_ending

        if href in old_links:
            print(None, "IS: old href")
            continue

        source_article = requests.get(href)
        source_article.raise_for_status()
        bsoup = BeautifulSoup(source_article.text, "html.parser")

        rege2 = re.compile('.*ab-test-article-body*.')
        content = bsoup.find('section', class_=rege2)
        if content == None or content.text == None or content.text == "" or content.text == [] or content == "":
            print(None, "IS: content")  # debug print
            continue
        text = content.text
        
        heading = bsoup.find('h1')
        if heading.text == None:
            print(None, "IS: heading")
            continue
        header = heading.text

        print("IS:", href) # debug print

        rege2 = re.compile('ab-test-ingress*.')
        p = bsoup.find('p', class_=rege2)
        if p == None:
            paragraph = ""
        else:
            paragraph = p.text

        time_utc = bsoup.find('time', itemprop="datePublished")
        date = time_utc.get('datetime')
        if date:
            dt_object = parser.parse(date)
            fin_zone = dt_object.astimezone(ZoneInfo("Europe/Helsinki"))
            date = fin_zone.strftime('%d.%m.%Y')
        else:
            fin_zone = datetime.now(ZoneInfo("Europe/Helsinki"))
            date = fin_zone.strftime('%d.%m.%Y')

        popularity = index+1
        provider = "IS"

        response = requests.get(image_src)

        if response.status_code == 200:
            # The content of the response contains the image binary data
            req_image = response.content

            # Specify the location and name of the file to save the image
            
            imagepath = f'static/images/{href.replace("/", "_")}.png'

            # Open a file in binary write mode and write the image data
            with open(imagepath, 'wb') as f:
                f.write(req_image)
            resize_image(imagepath, imagepath, 200, 125)
            print("Image done")

        
        df = pd.DataFrame({
                    "popularity": popularity,
                    "header": header,
                    "href": href,
                    "date": date,
                    "provider": provider,
                    "paragraph": paragraph,
                    "imagepath": imagepath,
                    "text": text,}, index=[len(articles)+1])
        
        articles.append(df)


def ScrapeHS(articles: list[pd.DataFrame]):

    old_links = []
    if articles:
        old_links = articles[0].to_dict('list')['href']

    # Get page
    # Choose Chrome driver
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    driver.get("https://www.hs.fi")
    # Extract description from page and print

    iframe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//iframe[@title="SP Consent Message"]')))
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[@title="OK"]'))).click()
    sleep(2)
    print("Waiting for few seconds...")
    # Get the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Set how many pixels you want to scroll each step
    step_size = 300

    # Gradually scroll down the page
    for y in range(0, total_height, step_size):
        driver.execute_script(f"window.scrollTo(0, {y});")
        sleep(0.1)  # Adjust sleep time as needed for the page to render.

    # Scroll to the very bottom to ensure the entire page is loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Now that the page is loaded, including dynamic content, get the page source
    html = driver.page_source
    driver.quit()

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    headlines = []
    # Now you can use BeautifulSoup as before to parse the page
    sections = soup.find('section', class_="w-full max-w-main lg:w-main")
    for section in sections:
        hs_articles = section.find_all('article')
        for hs_article in hs_articles:
            img_tag = hs_article.img
            if img_tag and 'src' in img_tag.attrs:
                image_src = img_tag['src']
                headline = hs_article.find('a', class_='block')
                headlines.append((headline,image_src))

    #section = soup.find('section', class_="flex justify-start sm:justify-center lg:justify-start")
    #headlines = section.find_all('a', href=True)

    already_seen = set()

    for index, (headline,image_src) in enumerate(headlines):
        if headline == None:
            continue
        if headline.text not in already_seen:
            already_seen.add(headline.text)
        else:
            print(None, "HS: seen already")
            continue

        href_ending = headline.get('href')
        
        if "http" in href_ending or "mainos" in href_ending or "html" not in href_ending:
            print(None, "HS: wrong type")
            continue
        href = "https://www.hs.fi"+href_ending

        if href in old_links:
            print(None, "HS: old href")
            continue
        
        source_article = requests.get(href)
        source_article.raise_for_status()
        bsoup = BeautifulSoup(source_article.text, "html.parser")

        rege1 = re.compile('.*ab-test-article-body*.')
        content = bsoup.find('section', class_=rege1)
        if content == None or content.text == None or content.text == "" or content.text == [] or content == "":
            print(None, "HS: content")
            continue
        text = content.text
        
        heading = bsoup.find('h1')
        if heading.text == None:
            print(None, "HS: heading")
            continue
        header = heading.text

        print("HS:", href) # debug print

        rege2 = re.compile('.*ab-test-ingress*.')
        p = bsoup.find('p', class_=rege2)
        if p == None:
            paragraph = ""
        else:
            paragraph = p.text

        time_utc = bsoup.find('time', itemprop="datePublished")
        date = time_utc.get('datetime')
        if date:
            dt_object = parser.parse(date)
            fin_zone = dt_object.astimezone(ZoneInfo("Europe/Helsinki"))
            date = fin_zone.strftime('%d.%m.%Y')
        else:
            fin_zone = datetime.now(ZoneInfo("Europe/Helsinki"))
            date = fin_zone.strftime('%d.%m.%Y')

        popularity = index+1
        provider = "HS"

        response = requests.get(image_src)

        if response.status_code == 200:
            # The content of the response contains the image binary data
            req_image = response.content

            # Specify the location and name of the file to save the image
            
            imagepath = f'static/images/{href.replace("/", "_")}.png'

            # Open a file in binary write mode and write the image data
            with open(imagepath, 'wb') as f:
                f.write(req_image)
            resize_image(imagepath, imagepath, 200, 125)
            print("Image done")

        df = pd.DataFrame({
                    "popularity": popularity,
                    "header": header,
                    "href": href,
                    "date": date,
                    "provider": provider,
                    "paragraph": paragraph,
                    "imagepath": imagepath,
                    "text": text,}, index=[len(articles)+1])
        
        articles.append(df)


def main():

    articles = []
    try:
        df_ex = read_data()
        articles.append(df_ex)
    except Exception as e:
        print(f"no previous articles: {e}\n")
    
    ScrapeYle(articles)
    ScrapeIS(articles)
    ScrapeHS(articles)
    df = pd.concat(articles)

    sorted_df = df.sort_values(by='popularity')
    write_data(sorted_df)
    filter_dates()
    updated_documents = read_data()
    documents = updated_documents["text"].tolist()
    lemmatize_documents(documents)
    
    documents = read_lemmatized_documents()
    convert_to_tagged(documents)
    tagged_docs = load_tagged()
    print("training the model:")
    create_vectors(tagged_docs)
    print("Training done!")

    #df.to_parquet('dynamic-datasets/articles.parquet')


if __name__ == "__main__":
    main()