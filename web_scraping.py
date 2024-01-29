from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os

if os.path.isfile("./dynamic-datasets/article_dataset.txt"):
    os.remove("./dynamic-datasets/article_dataset.txt")
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
            if content == None or content.text == None or content.text == "" or content.text == []:
                print(None)  # debug print
                continue
            print(content.text) # debug print

            text = content.text
            popularity = index+1
            provider = "Yle"
            header = headline.text
            
            df = pd.DataFrame({
                "popularity": popularity,
                "header": header,
                "href": href,
                "text": text,
                "provider": provider}, index=[len(articles)])
            
            articles.append(df)
            file = open("dynamic-datasets/article_dataset.txt", mode="a", encoding='utf-8')  # append mode
            file.write(f'<article name="{header}" href="{href}">\n')
            file.write(text)
            file.write(f'\n</article>\n')
            file.close()

            #print(f"{popularity}: {header}, {href}\n")
            #header_size = re.findall("h[1-6]", str(headline))[0]
            #news_object.NewsArticle(headline.text, article_link, header_size, news_site['provider'])

    print(len(headlines))  # debug print
    print(len(already_seen)) # debug print
 

def main():

    articles = []
    ScrapeYle(articles)
    df = pd.concat(articles)
    df.to_excel('dynamic-datasets/articles_excel.xlsx', index=True)


if __name__ == "__main__":
    main()