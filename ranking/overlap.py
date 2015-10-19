# -*- coding: utf-8 -*-
import textmanip


def overlap_search(out_file='overlap.top'):
    '''
    Evaluate document relevance with respect to query by calculating overlap
    in terms between them.
    '''
    #get all documents
    all_documents, term_dictionary = textmanip.get_documents()
    all_queries = textmanip.get_queries()


    #find the overlap between each query and the all_documents
    queryDocList = list()                   		#for each query, it includes the similarity of that query with every document
    for queryDict in all_queries:
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

