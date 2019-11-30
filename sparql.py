import requests, json

def sparql(domain, query):
    url = 'http://%s/sparql' % domain
    response = requests.post(url, data={'print': True, 'query': query})
    if response:
        try:
            response = response.json()
            for binding in response.get('results', {}).get('bindings', []):
                abstract = binding.get('abstract',{}).get('value')
                # english version
                if abstract[-3:-1] == "en":
                    return abstract
        except Exception as e:
            print(response)
            raise e


if __name__ == '__main__':
    import sys
    try:
        _, DOMAIN, QUERY = sys.argv
    except Exception as e:
        print('Usage: python sparql.py DOMAIN QUERY')
        sys.exit(0)

    sparql(DOMAIN, QUERY)
