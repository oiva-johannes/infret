from sklearn.feature_extraction.text import CountVectorizer
#import web_scraping
import re
import numpy as np
from utils.utils import read_data


def search(file_path):

    df_ex = read_data(file_path)
    documents = df_ex["text"].tolist()
        
    cv = CountVectorizer(lowercase=True, binary=True)
    sparse_matrix = cv.fit_transform(documents) # create sparse matrix to save space
    sparse_td_matrix = sparse_matrix.T.tocsr() # convert the matrix to CSR (ordered by terms) and transpose it, creating an inverted index
    t2i = cv.vocabulary_ # creates a dictionary with terms as keys and term-indices as values
    
    query(sparse_td_matrix, t2i, documents) # run the actual query

def query(sparse_td_matrix, t2i, documents): # make the queries run in a loop

    while True:
        query = input("Please type your query in the format 'word operator word', 'quit' exits: ")
        if query == "quit":
             break
        print()
        
        query_result(query, sparse_td_matrix, t2i, documents) 
        #test_query(query, sparse_td_matrix, t2i) # for testing and debugging the query
        
d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}          # operator replacements

def rewrite_token(t, sparse_td_matrix, t2i):
    if t in t2i or t in d: # check that the query word actually exists in the vocabulary
        return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense
    
    else: # if it doesn't exist, returns a string that will create a numpy array with only zeroes, 
        # when evaluated to prevent attribute error in the eval function
        return f"np.zeros((1, {sparse_td_matrix.shape[1]}), dtype = int)" # default type is float, convert to integer
    
def rewrite_query(query, sparse_td_matrix, t2i): # rewrite every token in the query
    return " ".join(rewrite_token(t, sparse_td_matrix, t2i) for t in query.split())

        
def test_query(query, sparse_td_matrix, t2i): # for testing the queries
            print("Query: '" + query + "'")
            print("Rewritten:", rewrite_query(query, sparse_td_matrix, t2i))
            print("Matching:", eval(rewrite_query(query, sparse_td_matrix, t2i))) # Eval runs the string as a Python command

def query_result(query, sparse_td_matrix, t2i, documents): # get the query result 
            hits_matrix = eval(rewrite_query(query, sparse_td_matrix, t2i)) # check how many matches there are
            hits_list = list(hits_matrix.nonzero()[1]) # convert the matches to a list

            print(f"Total number of matched documents: {len(hits_list)}") # print the total amount of matches
                
            for i, doc_idx in enumerate(hits_list[:5]): # enumerate the documents 
                document = documents[doc_idx]
                sentences = re.split(r'(?<=[.!?])\s+', document) # split the documents to sentences, using positive lookbehind
                
                n = 3 # number of sentences to be shown of each document
                first_n_sentences = sentences[:n]
                print(f"Match #{i + 1} (first {n} sentences):\n {' '.join(first_n_sentences)}") # print the number of the match
                # and the specified number of sentences
                print()
    

def main():

   search("./dynamic-datasets/article_dataset.xlsx")
   
if __name__ == "__main__":
    main()
