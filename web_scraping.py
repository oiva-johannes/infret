from bs4 import BeautifulSoup
import requests
import re
import news_object


def ScrapeYle():

    try:
        source = requests.get("https://yle.fi/")
        source.raise_for_status() #Raises an error if there is a problem with the url
        
        soup = BeautifulSoup(source.text, "html.parser")
        headlines = soup.find_all(re.compile('h[1-6]')) #Find all the headers 
        
        word = "Venä[jä|l]"
        already_seen = set()

        for headline in headlines:
            if re.search(fr"\b{word}\w*\b", headline.text): #Matches all the headlines with the specified word
                if headline.text not in already_seen:
                    already_seen.add(headline.text)
                    link = "https://yle.fi" + re.findall("/[a-z]/[0-9][0-9]-[0-9]+", str(headline))[0]
                    header_size = re.findall("h[1-6]", str(headline))[0]
                    news_object.NewsArticle(headline.text, link, header_size)

    except Exception as e:
        print(e)


ScrapeYle()
news_object.NewsArticle.show()
