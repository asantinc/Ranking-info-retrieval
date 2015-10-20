# -*- coding: utf-8 -*-
import textmanip
import sys
import numpy
import math

K = 2

def tfidf(word_dict, queries, documents, doc_lengths):
    '''
    Calculate tf.idf score for all queries with every doc available
    '''
    query_doc_similarities = list()	   				#index it by list[query_i][doc_j]
    avg_doc_len = numpy.average(doc_lengths)

    for query_counter, query_dic in enumerate(queries):
        query_doc_similarities.insert(query_counter, list())		#store similarities between this query and all docs in this list

        for doc_counter, doc_dict in enumerate(documents):
            similarity = 0
            doc_len = doc_lengths[doc_counter]
            fudge = (K*doc_len)/avg_doc_len

            for word in query_dic:
                if word in doc_dic:				#if not in the document, similarity value added by this word is zero
                    frequencyInDoc = doc_dic[word]
                    inverseDocFrequency = word_dict[word][1]
                    IDF = math.log(len(documents)/inverseDocFrequency)
                    TF_Doc = frequencyInDoc/(frequencyInDoc+fudge)
                    TF_Query = query_dic[word]
                    similarity += TF_query*TF_Doc*IDF
            #insert similarity at this doc's position in the current queries' list
            query_doc_similarities[query_counter].append(similarity)
    return query_doc_similarities


def tfidf_search(out_file='overlap.top'):
    '''
    Evaluate document relevance with respect to query by calculating overlap
    in terms between them.
    '''
    #get all documents and queries
    all_documents, term_dictionary, doc_lengths = textmanip.get_documents()
    all_queries = textmanip.get_queries()

    #calculate the tfidf weigthed sum for each document query pair
    query_doc_similarities = tfidf(word_dict, queries, documents, doc_lengths)
    textmanip.outputResults(query_doc_similarities, 'tfidf.top')


if __name__ == '__main__':
    tdidf_search()

