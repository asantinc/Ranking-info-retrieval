# Search engine for text

#Overview
This project implements the following basic algorithms for document-query similarity computation and ranking:
- **Overlap**: uses the overlap between non-capitalized words to rank the documents relative to a given query
- **Tf-idf**: uses tf-idf as the weighting function for words and the weighted sum as the similarity function between the document and the query s(Q, D)
- **Rocchio**: As in 2, this algorithm uses td-idf and the weighted sum formula for an initial ranking, but then optimizes the original query using Rocchio’s algorithm

report.pdf contains further description of the implementation and key results.

#The Code
The code is found in the ranking/ folder. The output of each algorithm is written to output_ranking/ folder into a file with name algo_name.top. 

The performance of each of the algorithms can be evaluated using the trec_eval program, also included under ranking/. To do so, from the command line run:
- trec_eval -o -c -M1000 truth.rel overlap.top
- trec_eval -o -c -M1000 truth.rel tfidf.top
- trec_eval -o -c -M1000 truth.rel best.top
The program prints a number of standard effectiveness measures for each algorithm.
