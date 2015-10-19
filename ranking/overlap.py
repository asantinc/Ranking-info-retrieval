# -*- coding: utf-8 -*-
import textmanip


def overlap_search(out_file='overlap.top'):
    '''
    Evaluate document relevance with respect to query by calculating overlap
    in terms between them.
    '''
    all_documents = list()
    term_dictionary = dict()

    #get the all_documents
    with open('data/docs.txt') as doc_file:
        for doc in doc_file:                        		
            docDictionary = dict()
            token_list = textmanip.cleanUpText(doc)

            for token in token_list:             		#add tokens to document and overall dictionaries
            if token in term_dictionary:
                term_dictionary[token] = term_dictionary[token]+1
                if token in docDictionary:
                docDictionary[token] = docDictionary[token]+1
                else:
                docDictionary[token] = 1
            else:                           		#include unseen token in both dicts
                term_dictionary[token] = 1
                docDictionary[token] = 1
            all_documents.append(docDictionary)

    #get the query tokens
    with open('data/qrys.txt') as query_file:
        myQueries = list()			   		#list of queryDictionaries
        for query in query_file:
            token_list = textmanip.cleanUpText(query)
            queryDict = dict()
            i = 0
            for t in token_list:
                if i == 0: 			    		#ignore the query number for all myQueries
                    i = 1
                else:
                    if t in queryDict:
                        queryDict[t]+=1
                    else:
                        queryDict[t] = 1
            myQueries.append(queryDict)

    #find the overlap between each query and the all_documents
    queryDocList = list()                   		#for each query, it includes the similarity of that query with every document
    for queryDict in myQueries:
        documentRankings = list()                 		#list with the number of similarities between each query_i  and every document
        for documentDict in all_documents:      		
                docGrade = 0                    	
                for word in queryDict:   			
                    if word in documentDict:    		#if the word is actually in the document dictionary, increase its value by one
                        docGrade += 1
                documentRankings.append(docGrade)		#store the ranking for the current document (relative to query_i)
        queryDocList.append(documentRankings)

    textmanip.outputResults(queryDocList, 'output_ranking/{}'.format(out_file))

if __name__ == '__main__':
    overlap_search()

