# Ranking-info-retrieval
## Retrieval engine based on tf-idf

This project implements the following basic algorithms for document-query similarity computation and ranking:
- **Overlap**: uses the overlap between non-capitalized words to rank the documents relative to a given query
- **Tf-idf**: uses tf-idf as the weighting function for words and the weighted sum as the similarity function between the document and the query s(Q, D)
- **Rocchio**: As in 2, this algorithm uses td-idf and the weighted sum formula for an initial ranking, but then optimizes the original query using Rocchio’s algorithm

The performance of each of the algorithms can be evaluated using the trec_eval program, also included. To do so, from the command line run:
     - trec_eval -o -c -M1000 truth.rel overlap.top
     - trec_eval -o -c -M1000 truth.rel tfidf.top
     - trec_eval -o -c -M1000 truth.rel best.top
The program prints a number of standard effectiveness measures for your algorithm.

report.pdf contains a description of the implemtation and the key results.
