from sklearn.feature_extraction.text import CountVectorizer
import web_scraping.py

def search():
    cv = CountVectorizer(lowercase=True, binary=True)
    sparse_matrix = cv.fit_transform()
                                     
    
