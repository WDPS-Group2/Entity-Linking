import requests
'''
example
"http://10.149.0.127:9200/freebase/label/_search?q=obama"
{
    "hits" : {
    "total" : 172,
    "max_score" : 6.014344,
    "hits" : [ {
      "_index" : "freebase",
      "_type" : "label",
      "_id" : "AVgvwvuvuV5CxvxAa2D1",
      "_score" : 6.014344,
      "_source" : {
        "resource" : "fbase:m.02mjmr",
        "label" : "Barack Obama"
      }
    }
'''

def search(domain, query):
    url = 'http://%s/freebase/label/_search' % domain
    try:
        response = requests.get(url, params={'q': query, 'size':20})
    except:
        return {}
    id_score_labels = {}
    if response:
        response = response.json()
        for hit in response.get('hits', {}).get('hits', []):
            freebase_label = hit.get('_source', {}).get('label')
            freebase_id = hit.get('_source', {}).get('resource')
            freebase_score = hit.get('_score')
            id_score_labels.setdefault(freebase_id, set()).add(freebase_score).add( freebase_label )
    return id_score_labels

if __name__ == '__main__':
    import sys
    try:
        _, DOMAIN, QUERY = sys.argv
    except Exception as e:
        print('Usage: python kb.py DOMAIN QUERY')
        sys.exit(0)

    for entity, labels in search(DOMAIN, QUERY).items():
        print (entity,labels)




