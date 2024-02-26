from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from nltk.tokenize import word_tokenize
from scipy.sparse import vstack
import pandas as pd
from libvoikko import Voikko
v = Voikko("fi")
from utils.utils import read_data



def search_documents(query: str, documents: list[str]) -> list[tuple]:

    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    query = query.split(" ")
    print(query)

    lemmatized_documents = lemmatize_documents(documents) # lemmatize also the documents so the documents and the query match
    arrays = []

    for q in query:

        q = q.lower().strip()
        if q[0] == '"' and q[-1] == '"': # checks if the query has double quotes
            q = q[1:-1] # removes the double quotes from the query
            print(q) # debug
            sparse_matrix = tfv.fit_transform(documents).T.tocsr()
            query_vec = tfv.transform([q]).tocsc()
            hits = np.dot(query_vec, sparse_matrix)
            arrays.append(hits)


        else: # if the word is not enclosed in double quotes, search for all matches for the lemmatized query
            voikko_dict = v.analyze(q)
            for q in voikko_dict:
                lemmatized_q = q.get("BASEFORM") # get the lemmatized query
            print(lemmatized_q) # debug
            sparse_matrix = tfv.fit_transform(lemmatized_documents).T.tocsr()
            query_vec = tfv.transform([lemmatized_q]).tocsc()
            hits = np.dot(query_vec, sparse_matrix)
            arrays.append(hits)


    hits = vstack(arrays)
    hits = hits.tocsc()
    if hits.nnz > 0: # check that the number of matches is positive
        ranked = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
        already_seen = set()
        ranked = [r for r in ranked if r[1] not in already_seen and not already_seen.add(r[1])]

        return ranked
    
    else:
        return []


def lemmatize_documents(documents: list[str]) -> list[str]: # tokenize all the documents and lemmatize them
    
    lemmatized_documents = []
    for document in documents:
        words = word_tokenize(document, language='finnish')
        lemmatized_words = []
        for word in words:
            voikko_dict = v.analyze(word)
            for word in voikko_dict:
                lemma = word.get("BASEFORM")
                lemmatized_words.append(lemma)
    
        lemmatized_document = ' '.join(lemmatized_words)
        lemmatized_documents.append(lemmatized_document)
    
    return lemmatized_documents


def main():

    df_ex = read_data()
    documents = df_ex["text"].tolist()
    headers = df_ex["header"].tolist()
    links = df_ex["href"].tolist()
    dates = df_ex["date"].tolist()

    while True:
        query = input('Please type your query, use double quotes for exact match ("quit" exits): ').strip()
        if query == "quit":
             break

        ranked = search_documents(query, documents)

        if len(ranked) != 0:
            print(f"\nThe search found {len(ranked)} document matches for your query: '{query}', with varying precisions.\nHere they are ranked in order from best to worst:\n")

            for i, article in enumerate(ranked):
                score = article[0]
                header = headers[article[1]]
                link = links[article[1]]
                date = dates[article[1]]

                print(f"MATCH #{i + 1} with the score of {score}:\n'{header}'\nON {date} FROM {link}\n")
        else:
            print(f"\n\nThe search did not find any document to match your query: '{query}'\n\n")


if __name__ == "__main__":

    main()
