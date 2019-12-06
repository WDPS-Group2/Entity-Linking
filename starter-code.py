import re
import string
from elasticsearch import search
from sparql import query_abstract
from sklearn.feature_extraction.text import TfidfVectorizer

#discard non-English words
def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
        
#calculate the cosine similarity 
def cosine_sim(text1, text2):
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0,1]
abstract_dict = {}
def query_candidate_abstract(entity):
    abstract = ""
    if abstract_dict.__contains__(entity):
        abstract = abstract_dict[entity]
    else:
        abstract = query_abstract(SPARQL, entity)
        abstract_dict[entity] = abstract
    return abstract  
def find_abstract_object(abstract):
    abstract_token = nltk.word_tokenize(abstract)
    abstract_pos_tag = nltk.pos_tag(abstract_token)
    obj = ""
    # noun phrase before the first verb is the object of the abstract
    for token in abstract_pos_tag:
        if token[1].startswith("VB"):
            break
        else:
            obj = obj + token[0]+" "
    return obj
    
#the following part should be included in the main function
#the entities are get after linking mentions to elasticsearch
#this part is to find the entity with the highest tfidf-score among the 20 candidate entities
Tfidf_score_max = 0
for entity,labels in entities:
  if isEnglish(entity):
    abstract = query_candidate_abstract(entity)
    score = 0
    if abstract != None:
        abstract_object = find_abstract_object(abstract)
        if abstract_object != "":
            if cosine_sim(abstract_object, entity) < 0.1:
                continue
            else:
                score = score + cosine_sim(abstract_object, entity)
        if score > Tfidf_score_max:
            Tfidf_score_max = score
            entity_score_max = entity
