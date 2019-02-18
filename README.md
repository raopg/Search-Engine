# CS121 Project 3
@Authors: Prateek Rao, Muizz Jivani

## About

This is a search engine that that indexes roughly 37497 from the ICS subdomain. The database, which contains the inverted index, is stored using MongoDB Documents API, and served using Python Flask API and the Jinja2 templating engine.

## Scoring Criteria

Two elements of token relevance in documents were registered in our inverted index:
1. Positional Score
2. TF-IDF Score

All queries and documents were tokenized to optmize storage and indexing.

## Ranked Retrieval

Ranked retrieval was generally based on a composite score, consisting of the sum of normalized TF-IDF and Positional Scoring.
Each query returns a fixed number of results(15).
For single-term queries, the top 15 documents who had the highest composite score was returned.
For multi-term queries, the top 3 terms for each query was first selected. Then, the remaining queries(out of 15) were selected as the highest scored documents among all three documents not already selected in the top 3 terms.


## Dependencies
1. pymongo
2. mongoengine
3. flask
4. mongodb
5. bs4
6. nltk

## Running the Flask Search Engine:
1. Install dependencies with **pip install -r requirements.txt**
2. Make a connection to the MongoDB client.
3. Load the data using commented scripts in index.py. Run them one by one.
4. Run the search engine by executing: **python3 app.py**


## Resources Used:
1. NLTK Documentation
2. BeautifulSoup Documentation
3. PyMongo Documentation
4. W3C Schools Guides


