import string
import numpy #average
import math #log
import re
from nltk.stem.snowball import SnowballStemmer

stopwordList = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now']


def cleanUpTextStem(text, nGrams):
    '''
    Remove punctuation as defined by python, lower case text and split into tokens
    Return word stems.
    '''
    p = re.compile('[\W]+')
    clean_text = p.sub(' ' , text)
    lower_clean_text = clean_text.lower()
    myText = lower_clean_text.split()
    clean_text_list = list()
    for word in myText:
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        stem = stemmer.stem(word)
        clean_text_list.append(stem)
    return textToReturn


def cleanUpText(text):
    '''Remove punctuation as defined by python, lower case text and split into token'
    '''
    p = re.compile('[\W]+')
    clean_text = p.sub(' ' , text)
    lower_clean_text = clean_text.lower()
    myText = lower_clean_text.split()
    return myText


def createListOfLinks(token_list):
    index = -1
    if ("references" in token_list):
        index = token_list.index("references")
    if (index != -1):						#there are no links
    	return token_list[index+1:]
    else:
	    return index
										

def isStopWord(word):
    return word in stopwordList


def outputResults(queryDocList, filename):
    '''
    Output results into filename.top - only output if query value is greater than zero. The format is the following
    Query_i  0  Document_number 0  docGrade 0
       1      0        1009      0    0.1234 0 
       1      0        1010      0    0.5678 0 
       2      0        1003      0    0.9876 0   
    '''
    with open(filename, 'w') as f:
        for query_no, documentGradeList in enumerate(queryDocList):
            for doc_no, documentGrade in enumerate(documentGradeList):
                f.write('{} 0 {} 0 {} 0 \n'.format(query_no, doc_no, documentGrade))


def tfidfWordWeighting(word, docId, wordDict, documents, docLengthList, averageDocLength):
    '''
    Calculate td.idf for a single word 
    '''
    numberOfDocuments = len(documents)
    docLength = docLengthList[docId]
    documentDict = documents[docId]
    k = 2
    fudgeFactor = (k*docLength)/averageDocLength
    #calculate the tf.idf
    if word in documentDict:
        frequencyInDoc = documentDict[word]
        inverseDocFrequency = wordDict[word][1]
        IDF = math.log(numberOfDocuments/inverseDocFrequency)
        TF_Doc = frequencyInDoc/(frequencyInDoc+fudgeFactor)
        return TF_Doc*IDF
    else:
        return 0
                          

def get_documents(doc_file='data/docs.txt'):
    '''
    Return inverted index for each document
    '''
    all_documents = list()
    term_dictionary = dict()
    docLengthList = dict()

    with open(doc_file) as doc_file:
        for docNumber, doc in enumerate(doc_file):                        		
            docDictionary = dict()
            token_list = textmanip.cleanUpText(doc)

            for token in token_list:             		#add tokens to document and overall dictionaries
                if token in term_dictionary:
                    term_dictionary[token] += 1
                    if token in docDictionary:
                        docDictionary[token] += 1
                    else:
                        docDictionary[token] = 1
                else:                           		#include unseen token in both dicts
                    term_dictionary[token] = 1
                    docDictionary[token] = 1
                    docLengthList[docNumber] += 1 	#increase list for every token
                all_documents.append(docDictionary)
    return all_documents, term_dictionary, docLengthList

    docLengthList = list()
    averageDocLength = 0
    docNumber = 0

    for doc in docFile:                        			
        docDict = dict()
        token_list = textmanip.cleanUpText(doc)
        docLengthList.insert(docNumber, 0)		
        for token in token_list:             	
            if token in wordDict:
                wordDict[token][0] = wordDict[token][0]+1 
                if token in docDict:				
                    docDict[token] = docDict[token]+1	
                else:
                    docDict[token] = 1				
                    wordDict[token][1] = wordDict[token][1]+1 	
            else:	
                wordDict[token] = [1,1] 	
                docDict[token] = 1			
        documents.append(docDict)
    docFile.close()                            			#close document file



def get_queries(q_file='data/qrys.txt'):
    '''
    Return inverted index for all queries
    '''
    all_queries = list()
    with q_file as query_file:
        for query in query_file:
            token_list = textmanip.cleanUpText(query)
            queryDict = dict()
            i = 0
            for t in token_list:
                if i == 0: 			    		
                    i = 1
                else:
                    if t in queryDict:
                        queryDict[t]+=1
                    else:
                        queryDict[t] = 1
            all_queries.append(queryDict)
    return all_queries


