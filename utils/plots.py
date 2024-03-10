from utils.utils import read_lemmatized_documents
import spacy
from collections import Counter
import matplotlib.pyplot as plt 
from libvoikko import Voikko
v = Voikko("fi")
nlp = spacy.load("fi_core_news_sm") # load the model that will be used for the task

def get_entities(documents: list, label: str): 
    entities = []
    for document in documents:
        doc = nlp(document.lower()) # parse the text with the loaded model
        for ent in doc.ents:
            if ent.label_ == label: # append all geopolitical entities to a list
                entities.append(ent.text)
    entities = [ent for ent in entities if ent != "suomi"]
        
    entity_freq = Counter(entities) # count the occurrences of each stemmed entity
        
    print(entity_freq) # debug 
    return entity_freq

def plot_entities_gpe(entity_freq, n):
    most_common_entities = entity_freq.most_common(n) # get the most common entities with their frequencies
    entities, frequencies = zip(*most_common_entities) # unpack the list and group entities and frequencies to their own variables

    fig, ax = plt.subplots(figsize=(8, 9))  # create a figure and axis object
    ax.set_facecolor('#292b2c')  # set the background color of the axis to black
    fig.set_facecolor('#292b2c')  

    plt.bar(entities, frequencies)    
    plt.title('Yleisimmin esiintyvät geopoliittiset entiteetit Ylen uutisissa', color='#dfdcd4') # add a title   
    plt.xlabel('Geopoliittiset entiteetit', color='#dfdcd4') # name the x-axis   
    plt.ylabel('Frekvenssi', color='#dfdcd4') # name of the y-axis
    
    plt.tick_params(axis='x', colors='#dfdcd4')
    plt.tick_params(axis='y', colors='#dfdcd4')
    plt.xticks(rotation=45)
    plt.show()
    
def plot_entities_person(entity_freq, n):
    most_common_entities = entity_freq.most_common(n)  # get the most common entities with their frequencies
    entities, frequencies = zip(*most_common_entities)  # unpack the list and group entities and frequencies to their own variables

    fig, ax = plt.subplots(figsize=(8, 9))  # create a figure and axis object
    ax.set_facecolor('#292b2c')  # set the background color of the axis to black
    fig.set_facecolor('#292b2c')  

    ax.bar(entities, frequencies)
    ax.set_title('Yleisimmin esiintyvät henkilöt Ylen uutisissa', color='#dfdcd4')  # add a title
    ax.set_xlabel('Henkilöt', color='#dfdcd4')  # name the x-axis
    ax.set_ylabel('Frekvenssi', color='#dfdcd4')  # name of the y-axis

    ax.tick_params(axis='x', colors='#dfdcd4')
    ax.tick_params(axis='y', colors='#dfdcd4')
    plt.xticks(rotation=45)
    plt.tight_layout()  # adjust the layout to prevent overlapping
    plt.show()
    
def main():
    documents = read_lemmatized_documents()
    entity_freq_gpe = get_entities(documents, "GPE")
    plot_entities_gpe(entity_freq_gpe, 10)
    plt.savefig('ner_plot_gpe.png')
    entity_freq_person = get_entities(documents, "PERSON")
    plot_entities_person(entity_freq_person, 10)
    plt.savefig('ner_plot_person.png')
    
    
if __name__ == "__main__":

    main()