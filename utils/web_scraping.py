from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from dateutil import parser
from utils import read_data, write_data


def ScrapeYle(articles: list[pd.DataFrame]):

    old_links = []
    if articles:
        old_links = articles[0].to_dict('list')['href']

    source = requests.get("https://yle.fi")
    source.raise_for_status() #Raises an error if there is a problem with the url

    soup = BeautifulSoup(source.text, "html.parser")
    headlines = soup.find_all('a', class_="underlay-link") #Find all the headers 

    already_seen = set()
    
    for index, headline in enumerate(headlines):
        if headline.text not in already_seen:
            already_seen.add(headline.text)
            
            href = re.findall('href.*\">', str(headline))[0]
            if "https://areena.yle.fi" in href:
                print(None, "wrong type")
                continue
            
            if "https://yle.fi" not in href:
                href = "https://yle.fi"+href[6:-2]
            else:
                href = href[6:-2]

            if href in old_links:
                print(None, "old href")
                continue
            
            source_article = requests.get(href)
            source_article.raise_for_status()
            bsoup = BeautifulSoup(source_article.text, "html.parser")

            content = bsoup.find('section', class_="yle__article__content")
            if content == None or content.text == None or content.text == "" or content.text == [] or content == "":
                print(None, "content")  # debug print
                continue

            print(href) # debug print

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


            df = pd.DataFrame({
                "popularity": popularity,
                "header": header,
                "href": href,
                "date": date,
                "provider": provider,
                "paragraph": paragraph,
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
    df = pd.concat(articles)

    sorted_df = df.sort_values(by='popularity')
    write_data(sorted_df)
    #df.to_parquet('dynamic-datasets/articles.parquet')


if __name__ == "__main__":
    main()