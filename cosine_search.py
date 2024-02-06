from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re


def read_data(f_path: str):

    f = open(file=f_path, mode='r', encoding='utf-8')
    text = f.read()
    f.close()
    documents = text.split("</article>")
    return documents


def search_documents(query: str, documents: str):

    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    sparse_matrix = tfv.fit_transform(documents).T.tocsr()
    query_vec = tfv.transform([query]).tocsc()

    hits = np.dot(query_vec, sparse_matrix)
    ranked = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
    print(f'\n\nThe search found {len(ranked)} document matches for your query: "{query}", with varying precisions. Here they are ranked in order from best to worst:\n\n')

    for i, article in enumerate(ranked):
        score = article[0]
        document = documents[article[1]]
        header = re.findall(r"name.*[0-9]", document)[0]
        print(f"Match #{i + 1} with the score of {score}:\n{header}\n")


def main():

    documents = read_data('./dynamic-datasets/article_dataset.txt')

    while True:
        query = input('Please type your query ("quit" exits): ').strip()
        if query == "quit":
             break

        search_documents(query, documents)


if __name__ == "__main__":

    main()
