from nltk import word_tokenize
import gensim
import spacy
from utils.utils import read_lemmatized_documents, read_articles_only
import pickle


nlp = spacy.load("fi_core_news_sm") # load the model that will be used for the task

def convert_to_tagged(documents: list):
    docs = []
    piped_documents = nlp.pipe(documents)
    for i, document in enumerate(piped_documents):
        filtered_doc = [token.text for token in document if not token.is_stop] # filter out all tokens that are stopwords
        doc = gensim.models.doc2vec.TaggedDocument(filtered_doc, [i]) # create Tagged Documents
        docs.append(doc)
            
    with open('pickle_tagged.pkl', 'wb') as file:
        pickle.dump(docs, file)


def load_tagged(file_name: str = 'pickle_tagged.pkl'):
    # Load the tagged documents from a file using pickle
    with open(file_name, 'rb') as file:
        tagged_docs = pickle.load(file)
    return tagged_docs

    
def create_vectors(tagged_docs: list): # create document vectors using the tagged documents
    model = gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=2, epochs=25, window=20) 
    model.build_vocab(tagged_docs)
    model.train(tagged_docs, total_examples=model.corpus_count, epochs=model.epochs)
    model.save('semantic_gensim_model')


def load_model(model_name: str = 'semantic_gensim_model'):
    return gensim.models.doc2vec.Doc2Vec.load(model_name)


def semantic_query(query: str, model: list, documents: list) -> list[tuple]:
    q = nlp(query)
    q_without_stopwords = [token.text for token in q if not token.is_stop]
    q_tokens = word_tokenize(' '.join(q_without_stopwords), language='finnish')
    query_vector = model.infer_vector(q_tokens)
    most_similar = model.dv.most_similar([query_vector])
    print(most_similar) 
    return most_similar

if __name__ == "__main__":
    # testing
    documents = read_lemmatized_documents()
    #convert_to_tagged(documents)
    #tagged_docs = load_tagged()
    #print("training model:")
    #create_vectors(tagged_docs)´

    #some test queries
    query = "stubb vaimo"
    original_documents = read_articles_only()
    semantic_query(query, load_model(), original_documents)
    