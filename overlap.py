# -*- coding: utf-8 -*-
import string
import textmanip
import sys

docFile = open("docs.txt")
myDocuments = list()
myDictionary = dict()

for doc in docFile:                        		#get the myDocuments
    docDictionary = dict()
    token_list = textmanip.cleanUpText(doc)

    for token in token_list:             		#add tokens to document and overall dictionaries
	if token in myDictionary:
	    myDictionary[token] = myDictionary[token]+1
	    if token in docDictionary:
		docDictionary[token] = docDictionary[token]+1
	    else:
		docDictionary[token] = 1
	else:                           		#include unseen token in both dicts
	    myDictionary[token] = 1
	    docDictionary[token] = 1
    myDocuments.append(docDictionary)
docFile.close()                            		#close document file

#get the query tokens
qfile = open("qrys.txt")  	    			#this filename comes from the console, provided by the user   
myQueries = list()			   		#list of queryDictionaries
for query in qfile:
    token_list = textmanip.cleanUpText(query)
    queryDict = dict()
    i = 0
    for t in token_list:
	if i == 0: 			    		#ignore the query number for all myQueries
	    i = 1
	else:
	    if t in queryDict:
		queryDict[t] = queryDict[t]+1
	    else:
		queryDict[t] = 1
    myQueries.append(queryDict)
qfile.close()                           		#close query file

							#find the overlap between each query and the myDocuments
queryDocList = list()                   		#for each query, it includes the similarity of that query with every document
for queryDict in myQueries:
    documentRankings = list()                 		#list with the number of similarities between each query_i  and every document
    for documentDict in myDocuments:      		#look at each document
	docGrade = 0                    		#all docs start with grade zero
	for word in queryDict:   			#check if each word in the query
	    if word in documentDict:    		#if the word is actually in the document dictionary, increase its value by one
		docGrade = docGrade+1
	documentRankings.append(docGrade)		#store the ranking for the current document (relative to query_i)
    queryDocList.append(documentRankings)
#output the results to output.top
textmanip.outputResults(queryDocList, 'overlap.top')





