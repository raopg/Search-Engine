import database
import tokens
from bs4 import BeautifulSoup
from collections import defaultdict
import math

RAW_DATA_FOLDER = 'WEBPAGES_RAW'
## The positional scoring metric is represented in the dictionary below. Depending on where the token appears, a score is given to the token.
## In the scoring function, a default score of 0.2, i.e, the token appears in the body is given to all tokens. 
## Note that positional scoring is cummulative. If a token appears in the header and in the body, then the score will be 0.55
## This metric is so chosen to give a token a perfect score of 1 if it appears in the title, body and a header.
POSITIONAL_SCORING_METRIC = {
    'header': 0.35,
    'title': 0.45,
    'body': 0.2
}

def create_soup(file):
    '''This function simply creates a bs4 object for a given html file
        @param file: an open file object in read mode
    '''
    return BeautifulSoup(file.read(),'html.parser')

def get_all_header_strings(soup):
    '''This function goes through the soup object and returns a concatenation of all texts appearing in any header tags in the file
        @param soup: a BeautifulSoup4 object
    '''
    result_str = ''
    for header_tag in ['h1','h2','h3','h4','h5','h6']:
        for each_tag in soup.find_all(header_tag):
            try:
                result_str += each_tag.get_text() #If there is no text in this tag, .get_text() function call throws an attribute error, which is handled in the next line
            except AttributeError:
                continue
    return result_str


def generate_positional_score(all_tokens, soup):
    '''This function goes through all the tokens for a given webpage, and determines its positional score by examining the webpage's soup object
        Using the POSITIONAL_SCORING_METRIC dictionary, it assigns a score to the token
        @param all_tokens: all the tokens appearing in a given webpage
        @param soup: the BeautifulSoup object for the webpage in question
    '''
    result = defaultdict(float)
    header_tokens = tokens.tokenize(get_all_header_strings(soup))
    try:
        title_tokens = tokens.tokenize(soup.title.get_text())
    except AttributeError:
        title_tokens = dict()
    for token, freq in all_tokens.items():
        result[token] += POSITIONAL_SCORING_METRIC['body'] 
        if(token in header_tokens.keys()):
            result[token] += POSITIONAL_SCORING_METRIC['header']
        if(token in title_tokens.keys()):
            result[token] += POSITIONAL_SCORING_METRIC['title']

    return result


def generate_tf_idf(query, num_docs, docs, hits):
    '''This function generates the tf-idf score for a given query
        @param query: The query whose tf-idf needs to be calculated
        @param num_docs: The total number of documents in the database
        @param hits: Number of documents in which the query term appears(for idf)

        The formula used here  => tf_idf = 
        (Frequency of query in document/Total number of tokens in doc) * ln(Total number of docs/ Number of docs in which query appears)
    '''
    result = defaultdict(float)
    freq = 0
    for doc in docs:
        document = database.Webpages.objects(docID = doc).first()
        result[document.docID] = freq/document.number_of_tokens * math.log(num_docs / hits)
    return result

def write_queries(query_score,path):
    '''This function writes the queries presented in a dictionary of query, score pairs for each doc.
        @param query_score: Dictionary of the tokens to be written mapped to their score for a document
        @param path: The docID of the document whose queries are being written

    The invertion of information and its indexing mainly takes place in this function.
    '''
    for query, score in query_score.items():
        database.write_query_word(query,path,score)

def add_tf_idf(num_docs):
    '''This function updates the positional score that is currently the score of all queries, to include the tf_idf calculated for each query.
        This function is written to accomodate for the fact that idf cannot be computed without knowing all the queries that we know exist in documents
        Of course, we can always query the Webpages documents and get a list of docs for which the query is a match. However, 
        this method is about N times faster, where N is the size of the corpus
        @param num_docs: The total number of documents in the database
    '''
    count = 0
    for query in database.QueryWord.objects:
        count+=1
        print(count)
        tf_idf_scores = generate_tf_idf(query, num_docs, query.doc_score.keys(),len(query.doc_score.items()))
        for docID, tf_idf in tf_idf_scores.items():
            query.doc_score[docID] += tf_idf
        query.save()

def read_corpus_into_db(crawled_dict):
    '''Using the bookkeeping dictionary, we write all of the webpage information into the database using this function.
        @param crawled_dict: The bookkeeping dictionary read from bookkeeping.json
    '''
    for path, url in crawled_dict.items():
        print("Processing:",path, ' ', url)
        soup = create_soup(open(RAW_DATA_FOLDER + '/' + path))
        try:
            title = soup.title.get_text()
        except AttributeError:
            title = ''
        all_tokens = tokens.tokenize(soup.get_text())
        print("Tokenized: ", title)
        database.write_webpage(path,url,title,all_tokens)
        
def print_index():
    '''This function prints the entire inverted index. It was a helper written to gauge the scoring metric early in the database loading process.
    '''
    for queryObj in database.QueryWord.objects:
        print(queryObj.name,'\t',end = '')
        for doc, score in queryObj.doc_score.items():
            print(doc, '->', score)
        print()

def prettify_url(url):
    '''This function shortes urls to be neatly presented in the search engine results
        @param url: The URL to be shortened.
    '''
    if len(url) <= 25:
        return url
    else:
        return url[:12] + '...' + url[-10:len(url)]

    