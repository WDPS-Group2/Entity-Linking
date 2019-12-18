from html2text import html2text
from nlp_preproc_spark import nlp_preproc
from elasticsearch import search
from sparql import query_abstract
from sklearn.feature_extraction.text import TfidfVectorizer
import math

KEYNAME = "WARC-TREC-ID"

def find_key(payload):
    key = None
    for line in payload.splitlines():
        if line.startswith(KEYNAME):
            key = line.split(': ')[1]
            return key;
    return '';

def split_records(stream):
    payload = ''
    for line in stream:
        if line.strip() == "WARC/1.0":
            yield payload
            payload = ''
        else:
            payload += line

vectorizer = TfidfVectorizer()
def cosine_sim(text1, text2):
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0,1]

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
# {token:[candidate Freebase entity IDs]}
entity_dict = {}
def search_candidate(token):
    entities = None
    if entity_dict.__contains__(token) and isEnglish(token):
        entities = entity_dict[token]
    else:
        entities = search(ELASTICSEARCH,token).items()
        entity_dict[token] = entities
    return entities#entity,id,score,label

# {FreebaseID:abstract}
abstract_dict = {}
def query_candidate_abstract(entity):
    abstract = ""
    if abstract_dict.__contains__(entity):
        abstract = abstract_dict[entity]
    else:
        abstract = query_abstract(SPARQL, entity)
        abstract_dict[entity] = abstract
    return abstract


if __name__ == '__main__':
    import sys
    try:
        _, INPUT, ELASTICSEARCH,SPARQL = sys.argv
    except Exception as e:
        print('Usage: python starter-code.py INPUT ELASTICSEARCH SPARQL')
        sys.exit(0)


    with open(INPUT, errors='ignore') as fo:
        for record in split_records(fo):
            key = find_key(record);
            if key != '':
                text = html2text(record)
                tagged_tokens = nlp_preproc(text)
                mentions_types = []
                entity_result_dict = {}
                for token in tagged_tokens:
                    if token not in mentions_types:
                        mentions_types.append(token)

                for token in mentions_types:
                    Tfidf_score_max = 0
                    entity_score_max = ""
                    entities = search_candidate(token[0])

                    for entity,labels in entities:
                        if labels['freebase_label'] == token[0]:
                            score = math.inf
                            Tfidf_score_max = score
                            entity_score_max = entity
                            break
                        abstract = query_candidate_abstract(entity)
                        score = labels['freebase_score']
                        if abstract != None:
                            score = score + cosine_sim(text,abstract)
                            # find the max score entity
                            if score > Tfidf_score_max:
                                Tfidf_score_max = score
                                entity_score_max = entity

                    if Tfidf_score_max != 0:
                        entity_result_dict[token[0]] = entity_score_max
                for token in tagged_tokens:
                    if entity_result_dict.__contains__(token[0]):
                        print( key + '\t' + token[0] + '\t' + entity_result_dict[token[0]])






