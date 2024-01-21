from bs4 import BeautifulSoup
import requests
import re

try:
    source = requests.get("https://yle.fi/")
    source.raise_for_status() #Raises an error if there is a problem with the url
    
    soup = BeautifulSoup(source.text, "html.parser")
    headlines = soup.find_all("h3") #Find all h3 headers 
    
    word = "Venä[jä|l]"
    
    for headline in headlines:
        if re.search(fr"\b{word}\w*\b", headline.text): #Matches all the headlines with the specified word
            print(headline.text)
   
except Exception as e:
    print(e)