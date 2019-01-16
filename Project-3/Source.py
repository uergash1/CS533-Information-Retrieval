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
import math

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

user_input = input("Insert the path for html file: ")
assert os.path.exists(user_input), "There is no html file at "+str(user_input)

path1 = user_input + '*.html'
DF1={}
#path = 'D:\Reviews\*.html'
files  = glob.glob(path1)
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
        if docID not in docDict.keys():
            docDict[docID]=0
        docDict[docID]+=1
        DF1[word]=docDict

filename1 = "./"+"Dictionary.csv"
filename2 ="./" +"Postings.csv"
filename3="./" +"DocsTable.csv"

dict_file = open(filename1, 'w', newline='')
postingfile= open(filename2, 'w', newline='')
docfile=open(filename3,'w', newline='')

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
    df = len(DF1[key])
    dataDict = [term, df, offset]
    dict_file_writer.writerow(dataDict) 
    
    for docID in DF1[key].keys():
        tf=DF1[key][docID]
        dataPost = [offset, docID, tf]
        postingfile_writer.writerow(dataPost) 
        offset=offset+1



for file in files:
    text = open(file).read()

    docID=int(os.path.basename(file)[:-5])%1000
    #docID=os.path.basename(file)
    
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





#***********************************  PART 3  ***************************************************

dictFilename = "Dictionary.csv"
postingFilename = "Postings.csv"
docTableFilename= "DocsTable.csv"
N = len([f for f in os.listdir(user_input) if os.path.isfile(os.path.join(user_input, f))]) #number of html documents
dictPath = user_input[:-8] + dictFilename
postingPath = user_input[:-8] + postingFilename
docTablePath = user_input[:-8] + docTableFilename


tfidf={}
while True:
	user_query_initial = input("Insert query: ")
	user_query = user_query_initial.lower()
	if user_query == "exit":
		break
	tokens = word_tokenize(user_query)
	for token in tokens:
		if token != "and" or token != "not" or token != "or":
			stemmedToken = PorterStemmer().stem(token)
			with open(dictPath) as dictCsvFile:
				dictCsv = csv.reader(dictCsvFile, delimiter=',')
				next(dictCsv)
				for dictRow in dictCsv:
					if stemmedToken == dictRow[0]:
						tfidf[stemmedToken] = {}
						with open(postingPath) as postCsvFile:
							postCsv = csv.reader(postCsvFile, delimiter=',')
							next(postCsv)
							for postRow in postCsv:
								startOffsetDict = int(dictRow[2])
								endOffsetDict = startOffsetDict + int(dictRow[1]) - 1
								offsetPost = int(postRow[0])
								if offsetPost >= startOffsetDict and offsetPost <= endOffsetDict:
									df = math.log10(N / int(dictRow[1]))
									tf = (1 + math.log10(int(postRow[2])))
									temp = df * tf
									docID = postRow[1]
									tfidf[stemmedToken][docID] = '%.3f' % temp


	#Normalization
	denominator={}
	os.chdir(user_input)
	for docID in glob.glob("*.html"):
		docID = str(int(docID[:-5])%1000)
		flag = False
		for row in tfidf:
			if docID in tfidf[row].keys():
				if docID in denominator.keys():
					denominator[docID] = float(denominator[docID]) + math.pow(float(tfidf[row][docID]), 2)
				else:
					denominator[docID] = math.pow(float(tfidf[row][docID]), 2)
				flag = True
		if flag == True:
			temp = math.sqrt(float(denominator[docID]))
			denominator[docID] = '%.3f' % temp 

	for token in tfidf:
		for docID in tfidf[token].keys():
			temp = float(tfidf[token][docID]) / float(denominator[docID])
			tfidf[token][docID] = '%.3f' % temp

	
	#Boolean scoring
	scores = {}
	for token in tokens:
		token = PorterStemmer().stem(token)
		if token == "and":
			boolOperand = "and"
			isFirstRowScores = True
		elif token == "not":
			boolOperand = "not"
		elif token == "or":
			boolOperand = "or"
			isFirstRowScores = True
		else:
			if boolOperand == "and":
				for docID in tfidf[token].keys():
					if isFirstRowScores == True:
						scores[docID] = float(tfidf[token][docID])
					elif docID in scores.keys():
						temp = float(scores[docID]) + float(tfidf[token][docID])
						scores[docID] = '%.3f' % temp

				for docID in list(scores):
					if docID not in tfidf[token].keys():
						del scores[docID]

				isFirstRowScores = False

			elif boolOperand == "not":
				for docID in tfidf[token].keys():
					if docID in list(scores):
						del scores[docID]

			elif boolOperand == "or":
				for docID in tfidf[token].keys():
					if docID in scores.keys():
						temp = float(scores[docID]) + float(tfidf[token][docID])
						scores[docID] = '%.3f' % temp
					else:
						scores[docID] = float(tfidf[token][docID])

	for docID in scores.keys():
		scores[docID] = float(scores[docID])

	#Scoring based on Doc table
	pResults = {}
	otherResults = {}
	with open(docTablePath) as docTableCsvFile:
		docTable = csv.reader(docTableCsvFile, delimiter=',')
		next(docTable)
		for docTableRow in docTable:
			docID = docTableRow[0]
			if docID in scores.keys():
				if docTableRow[4] == "P":
					pResults[docID] = scores[docID]
				else:
					otherResults[docID] = scores[docID]

	finalScores = {}

	if bool(pResults):
		sorted(pResults.values())
		for docID in pResults.keys():
			finalScores[docID] = pResults[docID]

	if bool(otherResults):
		sorted(otherResults.values())
		for docID in otherResults.keys():
			finalScores[docID] = otherResults[docID]


	counter = 1
	output = open(user_input[:-8] + "output.txt", "w+")
	output.write("Query: " + user_query_initial + "\n")
	if bool(finalScores):
		with open(docTablePath) as docTableCsvFile:
			docTable = csv.reader(docTableCsvFile, delimiter=',')
			next(docTable)
			for docTableRow in docTable:
				docID = docTableRow[0]
				if docID in finalScores.keys():
					title = str(docTableRow[1])
					reviewer = str(docTableRow[2])
					snippet = str(docTableRow[3])
					rate = str(docTableRow[4])
					headline = "****************RESULT #" + str(counter) + "****************"
					print(headline)
					print("DocID: " + str(docID))
					print("Title: " + title)
					print("Reviewer: " + reviewer)
					print("Snippet: " + snippet)
					print("Rate: " + rate)
					print("\n")

					output.write(headline + "\n")
					output.write("DocID: " + str(docID) + "\n")
					output.write("Title: " + title + "\n")
					output.write("Reviewer: " + reviewer + "\n")
					output.write("Snippet: " + snippet + "\n")
					output.write("Rate: " + rate + "\n")
					output.write("\n")

					counter = int(counter) + 1
	else:
		print("NO RESULT\n")
		output.write("NO RESULT\n")
	output.close()