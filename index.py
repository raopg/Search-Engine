import json
import re
import sys
from collections import defaultdict
import scripts
import tokens

book_keeping_filename = 'bookkeeping.json'

NUMBER_OF_DOCS = 0

#First, we read the bookkeeping.json file into a dictionary using the json module. This will help us load the corpus into the database
with open(scripts.RAW_DATA_FOLDER + '/' + book_keeping_filename,'r') as file:
    bookkeeper = json.load(file)

# for k,v in crawled_dict.items():
#     print(k,' : ',v)



def get_top_fifteen(hits):
    '''This function takes the top 50 hits of each of the query tokens and computes the composite score of all the results combined.
        All the results are written into a common dictionary, and their scores added. Thus, the webpages with more than one hits will naturally
        bubble up the top of the dictionary.
        @param hits: A dictionary mapping each query token to its dictionary of hits.
    '''
    result = defaultdict(float)

    for query, hit_dict in hits.items():
        result = {**result, **get_top_three(hit_dict)}
    
    if(len(result.keys()) < 15):
        for query,hit_dict in hits.items():
            for hit, score in hit_dict.items():
                result[hit] = score

    return dict(sorted(result.items(), key = lambda x: x[1], reverse = True)[:15])

def get_top_three(hits):
    '''This function takes the top 50 hits and gives the top 3 hits'''
    return dict(sorted(hits.items(), key = lambda x: x[1], reverse=True)[:3])
def create_engine_info(important_hits):
    '''This function takes the top 15 hits and structures the data to be accessed by the frontend Jinja2 templating engine
        @param important_hits: The top 15 hits for the query_string.
    '''
    result = list(defaultdict(str))
    for docID,score in important_hits.items():
        doc = scripts.database.Webpages.objects(docID = docID).first()
        result.append({'url' : 'https://' + doc.url,'title': doc.title, 'pretty_url' : scripts.prettify_url(doc.url)})
    return result


def handle_query(query_str):
    '''This function is called when a query is presented. It tokenizes the query, and generates the results for the query
        @param query_str: The string entered by the user which represents the query.
    '''
    query_tokens = tokens.tokenize(query_str)
    all_hits = defaultdict()
    if len(query_tokens) == 0:
        raise KeyError()
    if len(query_tokens.items()) == 1:
        for query in query_tokens.keys():
            top_fifteen = dict(sorted(scripts.database.get_webpages(query).items(), key = lambda x: x[1], reverse = True)[:15])
        return create_engine_info(top_fifteen)
    for query in query_tokens.keys():
        hits = scripts.database.get_webpages(query)
        if hits == None or hits == {}:
            continue
        all_hits[query] = dict(sorted(hits.items(), key = lambda x: x[1], reverse=True)[:50])
    top_fifteen = get_top_fifteen(all_hits)
    return create_engine_info(top_fifteen)




if __name__  == "__main__":
    ##Uncomment the following code seperately and run them to populate the database with the raw data
    ##Be sure to read the docstring for each of these functions before running
    scripts.database.make_connection('cs121project3','localhost',port = 27017)
    #scripts.read_corpus_into_db(bookkeeper)
    
    NUMBER_OF_DOCS = scripts.database.Webpages.objects.count()
    # count = 0
    # for doc in scripts.database.Webpages.objects:
    #     count += 1
    #     print("COUNT", count)
    #     query_score = scripts.generate_positional_score(doc.tokens, scripts.create_soup(open(scripts.RAW_DATA_FOLDER + '/' + doc.docID)))
    #     scripts.write_queries(query_score,doc.docID)
    

    # scripts.add_tf_idf(NUMBER_OF_DOCS)
    # print_index()
    # query = input("Enter query:")
    # results = handle_query(query.lower())
    # for info in results:
    #     print(info['url'])
   

    
    


    print(scripts.database.Webpages.objects.count())
    print(scripts.database.QueryWord.objects.count())
