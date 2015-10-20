# -*- coding: utf-8 -*-
import string
import textmanip
import sys
import numpy
import math
import operator 
import copy 
import tfidf

########################################################################
# Implementation of Rocchio's algorithm algorithm for document retrieval
########################################################################

A = 4
B = 8
K = 2
if len(sys.argv) == 2:
    rel_docs = int(sys.argv[1])        
else:
    rel_docs = 13       


def rocchio():
    all_documents, term_dictionary, doc_lengths = textmanip.get_documents()
    all_queries = textmanip.get_queries()
    avg_doc_len = numpy.average(doc_lengths)

    #calculate the tfidf weigthed sum for each document query pair
    query_doc_similar_list = tfidf.tfidf(term_dictionary, all_queries, all_documents, doc_lengths)

    #1. Get top relevant docs
    most_rel_docs = list()
    for q, query in enumerate(all_queries):					
        if len(all_documents)<10:
            rel_docs = 2 if len(all_documents)>=2 else len(all_documents)
        most_rel_docs.append((sorted(query_doc_similar_list[q]))[:rel_docs], reverse=True) 
        
    #2. Calculate all the TFIDF of the words in the relevant all_documents
    #	Add the values together: for every word, add up the weight given to it by each document
    #	Get the 10 most important words
    #   Add those words to the query
    #   Run TFIDF again with new query
    query_weight_list = list()				
    for docList in most_rel_docs:			
        doc_weights = list()				
        for doc in docList:				
            currentDocDict = all_documents[doc]		
            word_weights = dict()				
            for word in term_dictionary:				
                word_weights[word] = textmanip.tfidfWordWeighting(word, doc, term_dictionary, all_documents, doc_lengths, avg_doc_len) 
            doc_weights.append(word_weights)
        query_weight_list.append(doc_weights)		

    #average out the values obtained for the weights accross all docs (per query) -> you get one weight list per query
    avg_query_w_list = list()			
    for i in range(len(all_queries)):				
        averageWordWeights = dict()				
        for word in term_dictionary:		
            addedWeight = 0
            for j in range(len(most_rel_docs[i])):		
                weightDict = query_weight_list[i][j]
                addedWeight += weightDict[word]		
            averageWordWeights[word] = addedWeight/(len(most_rel_docs[i])*1.00) 
        avg_query_w_list.append(averageWordWeights)		

    rocchio_q = copy.deepcopy(all_queries)
    for i in range(len(rocchio_q)):
        #get the max weighted words in the avg_query_w_list[i] dictionary
        sortedListOfWords = sorted(avg_query_w_list[i].items(), key=operator.itemgetter(1), reverse=True)
        
        wordsInTheRelevantDocs = list()
        for j in range(len(sortedListOfWords)):
            wordsInTheRelevantDocs.append(sortedListOfWords[j][0])
            for word in rocchio_q[i]:
                if word not in wordsInTheRelevantDocs:
                    rocchio_q[i][word] = (A*(rocchio_q[i][word]))
                
        for j in range(len(sortedListOfWords)):
            wordToAdd = sortedListOfWords[j][0]
            weightToAdd = sortedListOfWords[j][1]

            if wordToAdd in rocchio_q[i]:
                rocchio_q[i][wordToAdd] = (A*(rocchio_q[i][wordToAdd]))+(B*(weightToAdd))
            else:
                rocchio_q[i][wordToAdd] = (B*(weightToAdd))

    queryDocSimilaryList = tfidf.tfidf(term_dictionary, rocchio_q, all_documents, doc_lengths)
    textmanip.outputResults(queryDocSimilaryList, 'best.top')


if __name__ == '__main__':
    rocchio()
