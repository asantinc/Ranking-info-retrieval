# -*- coding: utf-8 -*-
import string
import textmanip
import sys
import numpy
import math
import operator 
import copy #deepcopy myQuery to the rocchioQuery

########################################################################
# Implementation of Rocchio's algorithm algorithm for document retrieval
########################################################################

if len(sys.argv) == 2:
    RELEVANT_DOC_NUMBER = int(sys.argv[1])        
else:
    RELEVANT_DOC_NUMBER = 13       
A = 4
B = 8


all_documents = list()
word_freq_dict = dict()					#keep track of all word frequency and idf
doc_len_list = list()
avg_doc_len = 0


with open('data/docs.txt') as doc_file:
    doc_number = 0
    for doc in doc_file:                        		
        docDict = dict()
        token_list = textmanip.cleanUpTextStem(doc, False)
        doc_len_list.insert(doc_number, 0)		#set up the length of this doc, will update as we see tokens
        for token in token_list:             		#add tokens to document and overall dictionaries
        if textmanip.isStopWord(token) == False:
            if token in word_freq_dict:
            word_freq_dict[token][0] = word_freq_dict[token][0]+1 
            if token in docDict:			#check if we've seen this token in this doc before
                docDict[token] = docDict[token]+1	
            else:
                docDict[token] = 1				#increase frequency to ONE: *first* encounter of token in this doc 
                word_freq_dict[token][1] = word_freq_dict[token][1]+1 	#increase idf: *first* encounter of token in this doc
            else:						  	#if not in word_freq_dict, we can't have seen it in this doc either
            word_freq_dict[token] = [1,1] 			  	#list will store frequency and the idf for token
            docDict[token] = 1				#frequency in this doc is 1
            doc_len_list[doc_number] = doc_len_list[doc_number]+1 #increase list for every token 
        doc_number += 1	
        all_documents.append(docDict)


with open('data/qrys.txt') as query_file:
    #get the query tokens
    myQueries = list()			    			#list of queryDictionaries
    for query in query_file:
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


#calculate the tfidf weigthed sum for each document query pair
myQueryDocSimilaryList = list()	   				
queryCounter = 0
avg_doc_len = numpy.average(doc_len_list)
k = 2
myQueryDocSimilaryList = textmanip.tfidf(word_freq_dict, myQueries, all_documents, doc_len_list)
rel_docs = RELEVANT_DOC_NUMBER

#############################################
#         ROCCHIO's algorithm               #
############################################# 
#1. Get the most highly ranked all_documents - these are our relevant all_documents
myRelevantDocsOverall = list()
for q in range(len(myQueries)):					#for every query
    myRelevantDocsOverall.append([])
    myDocRanking = myQueryDocSimilaryList[q]  			#get the doc rankings
    if (len(all_documents)<10):
	rel_docs = 2
    for i in range(rel_docs):
	index = myDocRanking.index(max(myDocRanking))		#get the doc ID of the highest ranked doc
	myRelevantDocsOverall[q].append(index)
	myDocRanking[index] = 0
	
	
#2. Calculate all the TFIDF of the words in the relevant all_documents
#	Add the values together: for every word, add up the weight given to it by each document
#	Get the 10 most important words
#   Add those words to the query
#   Run TFIDF again with new query
myQueryWeightList = list()				#store the word weights per doc per query
for docList in myRelevantDocsOverall:			#keeps list of relevant all_documents per query
    docWeightList = list()				#will store the weights of words for a single document
    for docIndex in docList:				#the id of a single relevant doc
	currentDocDict = all_documents[docIndex]		#get the actual docDictionary given the docIndex
	wordWeightDict = dict()				# a dictionary to store the weights of the words for this document
	for word in word_freq_dict:				#lgive a weight to every word in the document
	    weight = textmanip.tfidfWordWeighting(word, docIndex, word_freq_dict, all_documents, doc_len_list, avg_doc_len) 
	    wordWeightDict[word] = weight
	docWeightList.append(wordWeightDict)
    myQueryWeightList.append(docWeightList)		

#average out the values obtained for the weights accross all docs (per query) -> you get one weight list per query
myAverageQueryWeightList = list()			#list will contain the average query weights per query to be added on
for i in range(len(myQueries)):				#look at each query 
    averageWordWeights = dict()				#dict will store the weights per word added over all docs
    for word in word_freq_dict:				#look through each word 
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

queryDocSimilaryList = textmanip.tfidf(word_freq_dict, rocchioQueries, all_documents, doc_len_list)
fileName = "best.top"
textmanip.outputResults(queryDocSimilaryList, fileName)



