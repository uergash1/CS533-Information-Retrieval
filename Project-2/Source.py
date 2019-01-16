import glob 
import os
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import urllib.request
import string
import sys
import os.path
import csv

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



DF1={}
path = '.\Reviews\*.html'
files  = glob.glob(path)
for file in files:
    words = open(file).read()
    words = clean_html(words)
    words = remove_punctuation(words)
    words = remove_single_letter(words)
    words = tokenization_removing_stopwords(words)
    words = porter_stemming(words)
    words = sorted(words)

    for word in words:
        if word not in DF1.keys():
            DF1[word]={}
        docDict=DF1[word]
        docID=int(os.path.basename(file)[:-5])%1000
        #print("==>",docID)
        if docID not in docDict.keys():
            docDict[docID]=0
        docDict[docID]+=1
        DF1[word]=docDict

filename1 = "./"+"Dictionary.csv"
filename2 ="./" +"Postings.csv"
filename3="./" +"DocsTable.csv"

dict_file = open(filename1, 'w')
postingfile= open(filename2, 'w')
docfile=open(filename3,'w')

dict_file_writer = csv.writer(dict_file, delimiter=',')
postingfile_writer = csv.writer(postingfile, delimiter=',')
docfile_writer=csv.writer(docfile,delimiter=',')

dict_header=['Term','df','offset']
dict_file_writer.writerow(dict_header) 

posting_header=["offset", "DocID","tf"]
postingfile_writer.writerow(posting_header)    
 
#Mention the header for the DocsTable.csv file
docs_header=["Filename","Title","Reviewer","Snippet","Rate"]
docfile_writer.writerow(docs_header)

offset = 0
for key in DF1:
    term=key
    #tf = len(set(DF1[key]))
    #tfList=[DF1[key][docKey] for docKey in DF1[key].keys()]
    #tf=sum(tfList)
    df = len(DF1[key])
    #docID = set(DF1[key].keys())
    dataDict = [term, df, offset]

    dict_file_writer.writerow(dataDict) 
    offset=offset+df
    for docID in DF1[key].keys():
        tf=DF1[key][docID]
        dataPost = [offset, docID, tf]
        postingfile_writer.writerow(dataPost) 



for file in files:
    text = open(file).read()
    #text = clean_html(text).strip()

    docID=int(os.path.basename(file)[:-5])%1000
    
    startT1 = text.find('/Title?')
    startT2 = text[startT1:].find('>')
    endT = text[startT1+startT2:].find('(')
    title = text[startT1+startT2+1 : startT1+startT2+endT]
    

    startR1 = text.find('ReviewsBy')
    startR2 = text[startR1:].find('>')
    endR = text[startR1+startR2:].find('<')
    reviewer = text[startR1+startR2+1 : startR1+startR2+endR]

    startS = text.find('Capsule review')
    if startS != -1:
        endS = text[startS:].find('<')
        snippet = text[startS + 15: startS + endS]
    else:
        startS = text.find('<P>')
        tokens = word_tokenize(text[startS + 3:])
        snippet = ' '.join(tokens[:50])
    snippet = clean_html(snippet)

    point1 = text.find('-4 to +4 scale')
    point2 = text.find('Capsule review')

    if point1 != -1:
        rate = text[point1 - 50 : point1]
        number = re.findall('[-+]?[0-9]+', rate)
        number = list(map(int, number))
        if not number:
            rate = 'NA'
        else:
            number = number[0]
            if number >= 0:
                rate = 'P'
            else:
                rate = 'N'
    elif point2 != -1:
        endS = text[point2:].find('<')
        snippet = text[point2 + 15: point2 + endS].lower()
        tokens = word_tokenize(snippet)
        countP = 0
        countN = 0
        if 'best' or 'exciting' or 'outstanding' in tokens:
            countP = countP + 1
        if 'dull' or 'boring' or 'disappointing' or 'failure' in tokens:
            countN = countN + 1
        if countP - countN >= 0:
            rate = 'p'
        else:
            rate = 'N'
    else:
        rate = 'NA'

    docTable = [docID, title, reviewer, snippet, rate]
    docfile_writer.writerow(docTable) 




