# Logs Analysis - Udacity
### Full Stack Web Development NanoDegree
_______________________
## About
This project is a log analysis tool that analyzes a web accessing log database and obtains some useful statistics, including:
1. **What are the most popular three articles of all time?** Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
2. **Who are the most popular article authors of all time?** That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
3. **On which days did more than 1% of requests lead to errors?** The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.
## Prerequisites
* Python 2.7.5 [(Download here)](https://www.python.org/downloads/)
* Vagrant [(Download here)](https://www.vagrantup.com/downloads.html)
* VirtualBox [(Download here)](https://www.virtualbox.org/wiki/Downloads)
* PostgreSQL [(Download here)](https://www.postgresql.org/download/)
## About the web accessing log database
* source: [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
### Description: 
The newsdata.sql database contains 3 tables
* The authors table includes information about the authors of articles.
* The articles table includes the articles themselves.
* The log table includes one entry for each time a user has accessed the site.

Once you have the data loaded into your database, connect to your database using `psql -d news` and explore the tables using the `\dt` and `\d table` commands and select statements.
* `\dt` — display tables — lists the tables that are available in the database.
* `\d table` — (replace table with the name of a table) — shows the database schema for that particular table.

## Quick Start
1. A vagrant machine with Python and PostgreSQL installed should be prepared in advance. (or follow the instructions [here](https://classroom.udacity.com/nanodegrees/nd004/parts/51200cee-6bb3-4b55-b469-7d4dd9ad7765/modules/c57b57d4-29a8-4c5f-9bb8-5d53df3e48f4/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0) to download a prepared [vagrant machine](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip))
2. Login to the vagrant machine.
```
cd <directory to the Vagrantfile of vagrant machine>
vagrant up
vagrant ssh
```
3. Download the database from previous section and load it.
```
createdb news
psql -d news -f newsdata.sql
```
4. Clone this repo, run the code, and the results would be printed.
```
python log_analysis.py
```
## What's inside `log_analysis.py`
* A class `Log_Analysis` having 3 methods: `top_3_articles()`, `top_3_authors()`, `p1_errs()`, corresponding to questions from **About** section
* A test function `test_log_analysis()` running the above methods one by one
## Design of code
### Question 1 and 2
Observing that: 
1. The slug column from the articles table is substring of the path column from the log table.
2. The author column from the articles table is exactly the id column from the authors table.
  
Therefore, the log table can be joined with the articles table using the clause "log.path like ('%' || articles.slug)", and this new table can be joined with the authors table using the clause "articles.author=authors.id".
  
Afterwards, each data from the log table would be referenced with an article title and the corresponding author.
  
Finally, we can sum up the article titles or the authors, and pick the highest three results as the answers.
### Question 3  
For this one, we need to calculate both the total number and the errors of the requests for each day, and then combine them together to derive the error rate. This can be done by calculate them individually from the log table and then join the results together. Finally we pick the data with ratio higher than 1% as the answer.
## Licience
The content of this repository is licensed under [GPLv3](https://choosealicense.com/licenses/gpl-3.0/) licience.



