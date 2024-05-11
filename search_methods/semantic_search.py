import torch
from utils.utils import read_lemmatized_documents
from sentence_transformers import SentenceTransformer, util
import numpy as np


def generate_semantic_embeddings():

    # supports Finnish language
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    # tokenizer = transformers.BertTokenizer.from_pretrained("TurkuNLP/bert-base-finnish-cased-v1")
    model.eval()
    if torch.cuda.is_available():
        model = model.cuda()
    else:
        print("cuda not available")
    documents = read_lemmatized_documents()
    print("generating embeddings...")
    corpus_embeddings = model.encode(documents, convert_to_tensor=True).cpu()
    np.savez_compressed("semantic_embeddings.npz", data=corpus_embeddings)


def bert_query(q: str):
    emb_file = np.load("semantic_embeddings.npz")
    corpus_embeddings = torch.from_numpy(emb_file["data"]).to("cpu")

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    query_embedding = model.encode(q, convert_to_tensor=True).cpu()

    # cosine similarity and torch.topk to find the highest 5 scores
    print("generating query scores")
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    most_similar = torch.topk(cos_scores, k=5)
    scores = [(score.item(), idx.item()) for score, idx in zip(most_similar[0], most_similar[1])]
    by_scores = sorted(scores, key=lambda x: x[0], reverse=True)
    return by_scores


if __name__=="__main__":
    # some test queries in Finnish
    queries = [
    "Kotkot on paras kana paikka Helsingissä.",
    "Siellä on myös banger musat.",
    "Ja sen sijanti kalliossa on mainio, kivan lähellä Helsingin Yliopistoa.",]
    
    generate_semantic_embeddings()

    result = bert_query(queries[0])
    print(result)
    result = bert_query(queries[1])
    print(result)
    result = bert_query(queries[2])
    print(result)
    result = bert_query("tyhmä")
    print(result)
