import sys
from collections import Counter
import re
import io
from nltk.corpus import stopwords

# STOPWORDS = set(stopwords('english'))
STOPWORDS = list(stopwords.words('english'))
def clean_string(raw_string):
    '''Build a list of words that appear in the raw string'''
    words = raw_string.lower()
    words = re.split(r'\W+|_', words)
    return words

def tokenize(raw_string):
    '''Store the tokens in a Counter object and eliminiates stopwords'''
    list_of_words = clean_string(raw_string)
    if list_of_words == None or list_of_words == []:
        return
    fdist = Counter()
    fdist.update([word for word in list_of_words if word != '' and word not in STOPWORDS])
    return fdist

if __name__ == "__main__":
    print("Don't run me!")
    quit()