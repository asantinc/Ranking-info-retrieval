# Ranking-info-retrieval
## Basic retrieval engine based on tf-idf

This project implements the following basic algorithms for document-query similarity computation and ranking:
- **Overlap**: uses the overlap between non-capitalized words to rank the documents relative to a given query
- **Tf-idf**: uses tf-idf as the weighting function for words and the weighted sum as the similarity function between the document and the query s(Q, D)
- **Rocchio**: As in 2, this algorithm uses td-idf and the weighted sum formula for an initial ranking, but then optimizes the original query using Rocchio’s algorithm

report.pdf contains a description of the implemtation and the key results.
