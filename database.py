import mongoengine
from schema import *
import time
from collections import defaultdict
## Establish connection



def make_connection(database_name, host, port):
    '''Makes a connection to the MongoDB client with the given parameters
        @param database_name: Name of the database in the collection
        @param host: where the DB is being hosted
        @param port: The port of the host to connect to.
    '''
    connect(database_name,host = host, port = port)



def write_query_word(query,documentID, score):
    '''Given a token, the document ID and the score, this function writes the docID and score into the QueryWord document corresponding to the token.
        If the token does not have a corresponding document, a new one will be created
        @param query: The token 
        @param documentID: The ID of the document containing the query
        @param score: The score associated with the document and the query
    '''
    if(QueryWord.objects(name=query).count() == 0):
        print("New query")
        newQuery = QueryWord(name = query)
        newQuery.doc_score[documentID] = score
        print(newQuery.name)
        newQuery.save()
    else:
        print("existing query")
        queryObj = QueryWord.objects(name=query).first()
        queryObj.doc_score[documentID] = score
        print(queryObj.name)
        queryObj.save()

def write_webpage(path, url,page_title,all_tokens):
    '''Given the docID, page title and a token frequency dictionary, this function writes a Webpages document correspoding to the doc ID.
        If the docID does not have a corresponding document, a new one will be created.
        @param path: The docID of the document
        @param url: The absoulute HTTPS URL for the document
        @param title: The title of the webpage
        @param all_tokens: All the tokens that appear in this document
    '''
    if(Webpages.objects(docID = path).count() == 0):
        print("New webpage")
        newWebpage = Webpages(docID = path,
                            title = page_title,
                            url = url,
                            tokens = all_tokens,
                            number_of_tokens = len(all_tokens.items()))
        print(newWebpage.url)
        newWebpage.save()
    else:
        print("Existing webpage")
        webpageObj = Webpages.objects(docID = path).first()
        for token, freq in all_tokens.items():
            webpageObj.tokens[token] += freq
        webpageObj.save()
    
def get_webpages(query_str):
    '''Given a SINGLE WORD query, this function returns the doc_score dictionary of the document
        @param query_str: A SINGLE WORD query
    '''
    queryListGenerator = QueryWord.objects(name = query_str)
    if(queryListGenerator.count() == 0):
        return None
    else:
        queryObj = queryListGenerator.first()
        return queryObj.doc_score
    


if __name__ == "__main__":
    make_connection('load_everything10', 'localhost',port = 27017)
    result = get_webpages('page')
    for docID, url in result.items():
        print(docID, '->', url)

    query = QueryWord.objects(name = 'page').first()
    for docID, score in query.doc_score.items():
        print(docID,'->',score)
        

