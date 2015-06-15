# -*- coding: utf-8 -*-
import string
import textmanip
import sys
import numpy
import math

docFile = open("docs.txt")
documents = list()
wordDict = dict()						#keep track of all word frequency and idf
docLengthList = list()
averageDocLength = 0
docNumber = 0

for doc in docFile:                        			#get the documents
    docDict = dict()
    token_list = textmanip.cleanUpText(doc)
    docLengthList.insert(docNumber, 0)				#set up the length of this doc, will update as we see tokens
    for token in token_list:             			#add tokens to document and overall dictionaries
	if token in wordDict:
	    wordDict[token][0] = wordDict[token][0]+1 
	    if token in docDict:				#check if we've seen this token in this doc before
		docDict[token] = docDict[token]+1	
	    else:
		docDict[token] = 1				#increase frequency to ONE: *first* encounter of token in this doc 
		wordDict[token][1] = wordDict[token][1]+1 	#increase idf: *first* encounter of token in this doc
	else:						  	#if not in wordDict, we can't have seen it in this doc either
	    wordDict[token] = [1,1] 			  	#list will store frequency and the idf for token
	    docDict[token] = 1					#frequency in this doc is 1
	docLengthList[docNumber] = docLengthList[docNumber]+1 	#increase list for every token
    docNumber = docNumber+1	
    documents.append(docDict)
docFile.close()                            			#close document file

#get the query tokens
qfile = open("qrys.txt")  	    				  
queries = list()			    			#list of queryDictionaries
for query in qfile:
    token_list = textmanip.cleanUpText(query)
    queryDict = dict()
    i = 0
    for t in token_list:
	if i == 0: 			    			#ignore the query number for all queries
	    i = 1
	else:
	    if t in queryDict:
		queryDict[t] = queryDict[t]+1
	    else:
		queryDict[t] = 1
    queries.append(queryDict)
qfile.close()                           			#close query file


#calculate the tfidf weigthed sum for each document query pair
queryDocSimilaryList = list()	   				#list[query_i][doc_j]
queryCounter = 0
averageDocLength = numpy.average(docLengthList)
k = 2
queryDocSimilaryList = textmanip.tfidf(wordDict, queries, documents, docLengthList)
textmanip.outputResults(queryDocSimilaryList, 'tfidf.top')






