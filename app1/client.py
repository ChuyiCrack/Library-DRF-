from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client   #Retrieving the algolias client

def get_index(index_name = 'Chuyi-Crack Chuyi-Crack_Book'):
    client = get_client()
    index = client.init_index(index_name)   #With the index_name we are retrieving all the model that we pass to the algolias page
    return index

def perform_search(query,**kwargs):
    index = get_index()
    params = {}
    tags=""
    if 'tags' in kwargs:
        tags = kwargs.pop('tags') or []
        if len(tags) > 0:
            params['tagFilters'] = tags

    index_filters = [f'{k}:{v}' for k,v in kwargs.items() if v != None]
    if len(index_filters) > 0:
        params['facetFilters'] = index_filters
    print(params)
    results = index.search(query,params)   #in the models of algolia and its search function we are retrieveng the filtering items acroding to the query that has been passed to the function
    return results