# Entity Linking

After the entity mentions in the document are extracted, we linked these mentions with their named entities in the Knowledge Base. This phrase can be divided into the following steps:

* **Query the Knowledge Base** input surface form of mentions to ElasticSearch to get 20 candidate named entities from FreeBase
* **Ranking the candidate named entities** add the score given by ElasticSearch according to the popularity and the score calculated by cosine similarity of candidates' abstract and the sentence including the mention, then rank candidates according to this final score
