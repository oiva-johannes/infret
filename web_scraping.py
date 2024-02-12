from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os
import datetime

if os.path.isfile("./dynamic-datasets/articles_excel.xlsx"):
    os.remove("./dynamic-datasets/articles_excel.xlsx")


def ScrapeYle(articles: list[pd.DataFrame]):

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
                continue
            
            if "https://yle.fi" not in href:
                href = "https://yle.fi"+href[6:-2]
            else:
                href = href[6:-2]

            print(href) # debug print    

            source_article = requests.get(href)
            source_article.raise_for_status()
            bsoup = BeautifulSoup(source_article.text, "html.parser")

            content = bsoup.find('section', class_="yle__article__content")
            if content == None or content.text == None or content.text == "" or content.text == [] or content == "":
                print(None, "skipped")  # debug print
                continue

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
            else:
                date = datetime.datetime.now().strftime('%Y-%m-%d')


            text = content.text
            popularity = index+1
            provider = "Yle"
            header = headline.text
            article_id = re.findall("/a/.*", href)[0][3:]
            article_id = article_id.replace("-", "")
    

            df = pd.DataFrame({
                "popularity": popularity,
                "header": header,
                "href": href,
                "date": date,
                "articleid": article_id,
                "provider": provider,
                "paragraph": paragraph,
                "text": text,}, index=[len(articles)])
            
            articles.append(df)
 

def main():

    articles = []
    ScrapeYle(articles)
    df = pd.concat(articles)
    df.to_excel('dynamic-datasets/articles_excel.xlsx', index_label="indexdf")
    #df.to_parquet('dynamic-datasets/articles.parquet')


if __name__ == "__main__":
    main()