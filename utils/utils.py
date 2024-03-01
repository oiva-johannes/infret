import pandas as pd
from nltk.tokenize import word_tokenize
from libvoikko import Voikko
v = Voikko("fi")
import csv

# if it isn't your first time running this app in you can comment these two out
import nltk
nltk.download('punkt')


def read_data(file: str = 'dynamic_datasets/articles_excel.xlsx') -> pd.DataFrame:

    df_ex = pd.read_excel(file)
    return df_ex


def write_data(df, file: str = 'dynamic_datasets/articles_excel.xlsx'):

    df.to_excel(file, index=False)


def read_lemmatized_documents(file: str = 'dynamic_datasets/lemmatized.csv') -> list:

    f = open(file, newline='')
    reader = csv.reader(f, delimiter=';')
    documents = list(reader)
    f.close()

    return documents[0]


def lemmatize_documents(documents: list[str], file: str = "dynamic_datasets/lemmatized.csv"):
    testi = True

    lemmatized_documents = []
    for document in documents:
        document = document.lower().strip().replace(".", " ").replace(",", " ").replace(":", " ").replace(";", " ").replace("/", " ")
        if testi:
            print("document:", document)
        words = word_tokenize(document, language='finnish')
        if testi:
            print("words:", words)
        lemmatized_words = []
        for word in words:
            word = word.strip()
            voikko_dict = v.analyze(word)
            if voikko_dict:
                bf_word = voikko_dict[0]["BASEFORM"]
            else:
                bf_word = word
            lemmatized_words.append(bf_word)

        if testi:
            print("lemmatized_words:", lemmatized_words)
        lemmatized_document = ' '.join(lemmatized_words)
        if testi:
            print("lemmatized_document:", lemmatized_document)
        lemmatized_documents.append(lemmatized_document)
        if testi: 
            print("lemmatized_documents:", lemmatized_documents)
            testi = False

    print(len(lemmatized_documents))
    f = open(file, 'w', newline='')
    wr = csv.writer(f, delimiter=';')
    wr.writerow(lemmatized_documents)
    f.close()


if __name__=="__main__":

    lemmatized = read_lemmatized_documents()
    print(len(lemmatized))
