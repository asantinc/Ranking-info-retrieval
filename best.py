# -*- coding: utf-8 -*-
import string
import textmanip
import sys
import numpy
import math
import operator #used to sort the document ranking by value to pick the highest ranked docs as relevant
import copy #deepcopy myQuery to the rocchioQuery


if len(sys.argv) == 2:
    RELEVANT_DOC_NUMBER = int(sys.argv[1])        
else:
    RELEVANT_DOC_NUMBER = 13       

A = 4
B = 8
myQueryFile = open('qrys.txt')
myDocFile = open('docs.txt')
myDocuments = list()
myWordDict = dict()					#keep track of all word frequency and idf
myDocLengthList = list()
myAverageDocLength = 0


docNumber = 0
for doc in myDocFile:                        		#get the myDocuments
    docDict = dict()
    token_list = textmanip.cleanUpTextStem(doc, False)
    myDocLengthList.insert(docNumber, 0)		#set up the length of this doc, will update as we see tokens
    for token in token_list:             		#add tokens to document and overall dictionaries
	if textmanip.isStopWord(token) == False:
	    if token in myWordDict:
		myWordDict[token][0] = myWordDict[token][0]+1 
		if token in docDict:			#check if we've seen this token in this doc before
		    docDict[token] = docDict[token]+1	
		else:
		    docDict[token] = 1				#increase frequency to ONE: *first* encounter of token in this doc 
		    myWordDict[token][1] = myWordDict[token][1]+1 	#increase idf: *first* encounter of token in this doc
	    else:						  	#if not in myWordDict, we can't have seen it in this doc either
		myWordDict[token] = [1,1] 			  	#list will store frequency and the idf for token
		docDict[token] = 1				#frequency in this doc is 1
	    myDocLengthList[docNumber] = myDocLengthList[docNumber]+1 #increase list for every token 
    docNumber = docNumber+1	
    myDocuments.append(docDict)
myDocFile.close()                            			#close document file

#get the query tokens
myQueries = list()			    			#list of queryDictionaries
for query in myQueryFile:
    token_list = textmanip.cleanUpTextStem(query, False)
    queryDict = dict()
    i = 0
    for t in token_list:
	if textmanip.isStopWord(token) == False:
	    if i == 0: 			    			#ignore the query number for all myQueries
		i = 1
	    else:
		if t in queryDict:
		    queryDict[t] = queryDict[t]+1
		else:
		    queryDict[t] = 1
    myQueries.append(queryDict)
myQueryFile.close()                           			#close query file


#calculate the tfidf weigthed sum for each document query pair
myQueryDocSimilaryList = list()	   				
queryCounter = 0
myAverageDocLength = numpy.average(myDocLengthList)
k = 2
myQueryDocSimilaryList = textmanip.tfidf(myWordDict, myQueries, myDocuments, myDocLengthList)



rel_docs = RELEVANT_DOC_NUMBER

#############################################
#         ROCCHIO's algorithm               #
############################################# 

#1. Get the most highly ranked myDocuments - these are our relevant myDocuments
myRelevantDocsOverall = list()
for q in range(len(myQueries)):					#for every query
    myRelevantDocsOverall.append([])
    myDocRanking = myQueryDocSimilaryList[q]  			#get the doc rankings
    if (len(myDocuments)<10):
	rel_docs = 2
    for i in range(rel_docs):
	index = myDocRanking.index(max(myDocRanking))		#get the doc ID of the highest ranked doc
	myRelevantDocsOverall[q].append(index)
	myDocRanking[index] = 0
	
	
#2. Calculate all the TFIDF of the words in the relevant myDocuments
#	Add the values together: for every word, add up the weight given to it by each document
#	Get the 10 most important words
#   Add those words to the query
#   Run TFIDF again with new query
myQueryWeightList = list()				#store the word weights per doc per query
for docList in myRelevantDocsOverall:			#keeps list of relevant myDocuments per query
    docWeightList = list()				#will store the weights of words for a single document
    for docIndex in docList:				#the id of a single relevant doc
	currentDocDict = myDocuments[docIndex]		#get the actual docDictionary given the docIndex
	wordWeightDict = dict()				# a dictionary to store the weights of the words for this document
	for word in myWordDict:				#lgive a weight to every word in the document
	    weight = textmanip.tfidfWordWeighting(word, docIndex, myWordDict, myDocuments, myDocLengthList, myAverageDocLength) 
	    wordWeightDict[word] = weight
	docWeightList.append(wordWeightDict)
    myQueryWeightList.append(docWeightList)		

#average out the values obtained for the weights accross all docs (per query) -> you get one weight list per query
myAverageQueryWeightList = list()			#list will contain the average query weights per query to be added on
for i in range(len(myQueries)):				#look at each query 
    averageWordWeights = dict()				#dict will store the weights per word added over all docs
    for word in myWordDict:				#look through each word 
	addedWeight = 0
	for j in range(len(myRelevantDocsOverall[i])):		#add up all of the weigths per word together
	    weightDict = myQueryWeightList[i][j]
	    addedWeight += weightDict[word]		#for every document j, add on its word weigth
	averageWeight = addedWeight/(len(myRelevantDocsOverall[i])*1.00)	#take the average of the sum
	averageWordWeights[word] = averageWeight
    myAverageQueryWeightList.append(averageWordWeights)		#for each query we will append a single new wordWeightDict 


#get the max weighted words
#add them to my query
#for A in range(0, 4):
#for B in range(4, 8):
counter = 0
rocchioQueries = copy.deepcopy(myQueries)
for i in range(len(rocchioQueries)):
    #get the max weighted words in the myAverageQueryWeightList[i] dictionary
    sortedListOfWords = sorted(myAverageQueryWeightList[i].items(), key=operator.itemgetter(1), reverse = True)
    
    wordsInTheRelevantDocs = list()
    for j in range(len(sortedListOfWords)):
	wordsInTheRelevantDocs.append(sortedListOfWords[j][0])
    
    for word in rocchioQueries[i]:
	if word not in wordsInTheRelevantDocs:
	    rocchioQueries[i][word] = (A*(rocchioQueries[i][word]))
    
    for j in range(len(sortedListOfWords)):
	wordToAdd = sortedListOfWords[j][0]
	weightToAdd = sortedListOfWords[j][1]
	if wordToAdd in rocchioQueries[i]:
	    rocchioQueries[i][wordToAdd] = (A*(rocchioQueries[i][wordToAdd]))+(B*(weightToAdd))
	#rocchioQueries[i][wordToAdd] = (weightToAdd)
	else:
	    rocchioQueries[i][wordToAdd] = (B*(weightToAdd))

fileName = "best.top"
queryDocSimilaryList = textmanip.tfidf(myWordDict, rocchioQueries, myDocuments, myDocLengthList)
textmanip.outputResults(queryDocSimilaryList, fileName)



