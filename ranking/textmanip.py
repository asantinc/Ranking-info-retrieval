import string
import numpy #average
import math #log
import re
from nltk.stem.snowball import SnowballStemmer


def cleanUpTextStem(text, nGrams):
   #Remove punctuation as defined by python, lower case text and split into token'
    p = re.compile('[\W]+')
    clean_text = p.sub(' ' , text)
    lower_clean_text = clean_text.lower()
    myText = lower_clean_text.split()
    textToReturn = list()
    for word in myText:
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
	stem = stemmer.stem(word)
        textToReturn.append(stem)
    return textToReturn


def cleanUpText(text):
   #Remove punctuation as defined by python, lower case text and split into token'
    p = re.compile('[\W]+')
    clean_text = p.sub(' ' , text)
    lower_clean_text = clean_text.lower()
    myText = lower_clean_text.split()
    return myText


def createListOfLinks(token_list):
    index = -1
    if ("references" in token_list):
	index = token_list.index("references")
    if ( index != -1 ):						#there are no links
	return token_list[index+1:]
    else:
	return index
										
def isStopWord(word):
    stopwordList = [u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now']
    return (word in stopwordList)

def tfidf(wordDict, queries, documents, docLengthList):
    queryDocSimilaryList = list()	   				#list[query_i][doc_j]
    queryCounter = 0
    averageDocLength = numpy.average(docLengthList)
    k = 2
    
    for queryDict in queries:
	queryDocSimilaryList.insert(queryCounter, list())		#store similarities between this query and all docs in this list
	numberOfDocuments = len(documents)
	docCounter = 0
	for documentDict in documents:
	    similarity = 0
	    docLength = docLengthList[docCounter]
            fudgeFactor = (k*docLength)/averageDocLength
	    for word in queryDict:
		if word in documentDict:				#if not in the document, similarity value added by this word is zero
		    #calculate the tf.idf
		    #add it to the similarity
		    frequencyInDoc = documentDict[word]
		    inverseDocFrequency = wordDict[word][1]
		    IDF = math.log(numberOfDocuments/inverseDocFrequency)
		    TF_Doc = frequencyInDoc/(frequencyInDoc+fudgeFactor)
		    TF_Query = queryDict[word]
		    similarity_temp = TF_Query*TF_Doc*IDF
		    similarity = similarity + similarity_temp
	    #insert similarity at this doc's position in the current queries' list
	    queryDocSimilaryList[queryCounter].append(similarity)
	    docCounter = docCounter+1
        queryCounter = queryCounter+1
    return queryDocSimilaryList



def outputResults(queryDocList, filename):
#output results into filename.top - only output if query value is greater than zero. The format is the following
# Query_i  0  Document_number 0  docGrade 0
#   1      0        1009      0    0.1234 0 
#   1      0        1010      0    0.5678 0 
#   2      0        1003      0    0.9876 0   
    f = open(filename, 'w')
    queryNo = 0
    for documentGradeList in queryDocList:
	queryNo = queryNo+1
	docNo = 0
        for documentGrade in documentGradeList:
	    docNo = docNo+1
	    f.write(str(queryNo))
	    f.write(' 0 ')
	    f.write(str(docNo))
	    f.write(' 0 ')
	    f.write(str(documentGrade))
	    f.write(' 0 ')
	    f.write('\n')
    f.close()


def tfidfWordWeighting(word, docId, wordDict, documents, docLengthList, averageDocLength):
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
                          
