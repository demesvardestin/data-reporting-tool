# Data Reporting Script

##### This is a simple script running python code, which connects to a database 
##### and performs a series of sql queries on the postgresql dialect. All methods
##### use the psycopg2 library.

## popular_articles()
##### This method retrieves the three most popular articles.
##### It connects to the database, performs the appropriate query, and returns
##### a list of results. It's also structured around conditionals to catch 
##### edge cases, and a for loop to format the output in english-friend structure.

## popular_authors()
##### This method is very similar to the first, but it retrieves the three most 
##### popular authors by article views.

## error_days()
##### This method returns the days when the request error rate was above 1%.
##### It is very similar to the previous two functions, but its sql query is a bit 
##### more complex.

# Installation

##### To run this script, you need to have a vm running on your OS, such as Vagrant. 
##### After cd'ing into your vagrantfile location, make sure the vm is running with the

```
vagrant up
```

##### command. Then log in with 

```
vagrant ssh
```
##### Then download the 
##### [database setup](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
##### Retrieve the newsdata.sql file and put it in the same directory as your vagrantfile.
##### Then from the cl, run:

```
python data_reporting_tool.py
```

##### This should produce results similar to the snippets in the example.txt file.
