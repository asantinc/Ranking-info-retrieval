# -*- coding: utf-8 -*-
'''Overlap scoring
Function to calculate score for each document by checking the overlap between each
query and all documents'''

import ranking.textmanip as textmanip

def overlap_search(out_file='overlap.top'):
    '''
    Evaluate document relevance with respect to query by calculating overlap
    in terms between them.
    '''
    #get all documents
    all_documents, _, _ = textmanip.get_documents()
    all_queries = textmanip.get_queries()

    #find the overlap between each query and the all_documents
    query_doc_list = list()
    for query_dict in all_queries:
        doc_rankings = list()
        for doc_dict in all_documents:
            doc_grade = 0
            for word in query_dict:
                if word in doc_dict:
                    doc_grade += 1
            doc_rankings.append(doc_grade)
        query_doc_list.append(doc_rankings)

    textmanip.outputResults(query_doc_list, 'output_ranking/{}'.format(out_file))

if __name__ == '__main__':
    overlap_search()

