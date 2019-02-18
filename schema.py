#This file represents the Schema for our Database. We have two MongoDB documents -  Webpages and QueryWords.
##Webpages
#The webpages document is created for each webpage in the corpus. It stores the docID, url, title and a dictionary of tokens with their frequency
#The webpage document also caches the total number of tokens in each webpage it instatiates.
##QueryWord
#This object stores the name of the token it represents, and a dictionary of docIDs matched with their score.
#The score is a composition, comprising of two parameters: positonal score, and tf-idf weight.


from mongoengine import *



class Webpages(Document):
    docID = StringField()
    url = StringField()
    title = StringField()
    tokens = DictField(IntField())
    number_of_tokens = IntField()


class QueryWord(Document):
    name = StringField(required = True,unique = True)
    doc_score = MapField(FloatField())



if __name__ == "__main__":
    q = QueryWord()
    w = Webpages()


