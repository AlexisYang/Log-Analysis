# Log-Analysis
How to test: 
1. Run log_analysis.py directly and it would print out the answers to the 3 questions one by one.
2. The class Log_Analysis has 3 methods: top_3_articles(), top_3_authors(), p1_errs(), corresponding to questions 1-3.

Design of code:
  Observed that: 
1. The slug column from the articles table is substring of the path column from the log table.
2. The author column from the articles table is exactly the id column from the authors table.
  Therefore, for question 1 and 2, the log table can be joined with the articles table using the clause "log.path like ('%' || articles.slug)", and this new table can be joined with the authors table using the clause "articles.author=authors.id".
  Afterwards, each data from the log table would be referenced with an article title and the corresponding author.
  Finally, we can sum up the article titles or the authors, and pick the highest three results as the answers.
  For question 3, we need to calculate both the total number and the errors of the requests for each day, and then combine them together to derive the error rate. This can be done by calculate them individually from the log table and then join the results together. Finally we pick the data with ratio higher than 1% as the answer.

