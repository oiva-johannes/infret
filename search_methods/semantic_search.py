from nltk import word_tokenize
import gensim
import spacy
from utils.utils import read_lemmatized_documents

nlp = spacy.load("fi_core_news_sm") # load the model that will be used for the task

def convert_to_tagged(documents: list):
    docs = []
    for i, document in enumerate(documents):
        document = nlp(document) # parse the text with the loaded model and tokenize
        filtered_doc = [token.text for token in document if not token.is_stop] # filter out all tokens that are stopwords
        doc = gensim.models.doc2vec.TaggedDocument(filtered_doc, [i]) # create Tagged Documents
        docs.append(doc)
            
    return docs

def process_query(queries: str, model: list, documents: list):
    for q in queries:
        print("Query:", q)
        q = nlp(q)
        q_without_stopwords = [token.text for token in q if not token.is_stop]
        q_tokens = word_tokenize(' '.join(q_without_stopwords), language='finnish')
        query_vector = model.infer_vector(q_tokens)
        most_similar = model.dv.most_similar([query_vector], topn=5)
        for doc_position, doc_score in most_similar:
            print(f"- {doc_score:.4f}  ({doc_position:>3})  {documents[doc_position][:100]}...")
        print()
    
def create_vectors(tagged_docs: list): # create document vectors using the tagged documents
    model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=100) 
    model.build_vocab(tagged_docs)
    model.train(tagged_docs, total_examples=model.corpus_count, epochs=model.epochs) 
    print("Done!")
    
    return model
    


if __name__ == "__main__":
    documents = read_lemmatized_documents()
    tagged_docs = convert_to_tagged(documents)
    model = create_vectors(tagged_docs)
    
    # some test queries
    queries = [
    "venäjä",
    "talous",
    "oppositio",
    "eriytyminen"
    ]

    process_query(queries, model, documents)
    