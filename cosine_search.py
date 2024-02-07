from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("finnish") # a stemmer for finnish


def read_data(f_path: str):

    f = open(file=f_path, mode='r', encoding='utf-8')
    text = f.read()
    f.close()
    documents = text.split("</article>")
    return documents


def search_documents(query: str, documents: str):
    
    if query[0] == '"' and query[-1] == '"': # checks if the query has double quotes
        query = query[1:-1] # removes the double quotes from the query
        tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
        sparse_matrix = tfv.fit_transform(documents).T.tocsr() # search the match from the unstemmed documents
        query_vec = tfv.transform([query]).tocsc() # use the unstemmed query
    
    else: # if the query is not enclosed in double quotes, search for all matches for the stem
        
        stemmed_query = stemmer.stem(query) # stem the query 
        print(stemmed_query) # debug print
    
        stemmed_documents = stem_documents(documents) # stem also the documents so the documents and the query match
    
        tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
        sparse_matrix = tfv.fit_transform(stemmed_documents).T.tocsr() # use stemmed documents
        query_vec = tfv.transform([stemmed_query]).tocsc() # also the stemmed query

    hits = np.dot(query_vec, sparse_matrix)
    if hits.nnz > 0: # check that the number of matches is positive
        ranked = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
        print(f'\n\nThe search found {len(ranked)} document matches for your query: "{query}", with varying precisions. Here they are ranked in order from best to worst:\n\n')

        for i, article in enumerate(ranked):
            score = article[0]
            document = documents[article[1]]
            header = re.findall(r"name.*[0-9]", document)[0]
            print(f"Match #{i + 1} with the score of {score}:\n{header}\n")
    else:
        print(f'\n\nThe search did not find any document to match your query: "{query}"\n\n')

def stem_documents(documents): # tokenize all the documents and stem them
    stem_documents = []
    for document in documents:
        words = word_tokenize(document)
        stem_words = [stemmer.stem(word) for word in words]
        stem_document = ' '.join(stem_words)
        stem_documents.append(stem_document)
    
    return stem_documents

def main():

    documents = read_data('./dynamic-datasets/article_dataset.txt')

    while True:
        query = input('Please type your query, use double quotes for exact match ("quit" exits): ').strip()
        if query == "quit":
             break
                
        search_documents(query, documents)


if __name__ == "__main__":

    main()
