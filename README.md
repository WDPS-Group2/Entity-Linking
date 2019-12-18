# Entity Linking

After the entity mentions in the document are extracted, we linked these mentions with their named entities in the Knowledge Base. This phrase can be divided into the following steps:

## Query the Knowledge Base
If the mention is English words, input surface form of mentions to ElasticSearch to get 20 candidate named entities with the highest popularity score from FreeBase
## Rank the candidate named entities
assign a score to each candidate, and rank them according to the score.
* check if the mention and the candidate is exactly the same, if so, set the score as Inf.
* calculated the cosine similarity of candidates' abstract and the context containing the mention, then assign a new score for every candidate -- the sum of the popularity score and the cosine similarity score. 
## Link the mention and the candidate
select the candidate with the highest score 
