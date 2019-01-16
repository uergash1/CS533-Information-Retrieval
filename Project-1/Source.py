from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import urllib.request
import re
import string
import sys
import os.path

#cleaning from html tags and case folding
def clean_html(source):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ' ', source)
  return cleantext.lower()

#removing punctuations
def remove_punctuation(source):
    return re.sub('['+string.punctuation+']', ' ', source)

#remove single letter from a string
def remove_single_letter(source):
    return ' '.join( [w for w in source.split() if len(w)>1] )

#tokenization and removing stop words
def tokenization_removing_stopwords(source):
    stopWords = set(('and', 'a', 'the', 'an', 'by', 'from', 'for', 'hence', 'of', 'the', 'with', 'in', 'within', 'who', 'when', 'where', 'why', 'how', 'whom', 'have', 'had', 'has', 'not', 'for', 'but', 'do', 'does', 'done'))
    tokens = word_tokenize(source)
    filteredTokens = []
    for token in tokens:
        if token not in stopWords:
            filteredTokens.append(token)
    return filteredTokens

#Porter's stemming
def porter_stemming(source):
    ps = PorterStemmer()
    stemmedTokens = []
    for token in source:
        stemmedTokens.append(ps.stem(token))
    return stemmedTokens

#reading html file
user_input = input("Enter the path of html file: ")
assert os.path.exists(user_input), "There is no html file at "+str(user_input)
htmlfile = open(user_input, 'r', encoding='utf-8')
source = htmlfile.read()
htmlfile.close()

source = clean_html(source)
source = remove_punctuation(source)
source = remove_single_letter(source)
source = tokenization_removing_stopwords(source)
source = porter_stemming(source)

#writing a list 
filePath = input("Enter the path where you want to save txt file: ")
fileName = input("Enter the name of txt file: ")
completeName = os.path.join(filePath, fileName+".txt")
file = open(completeName, "w")
for token in source:
  file.write("%s\n" % token)
file.close()