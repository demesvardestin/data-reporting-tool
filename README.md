## Data Reporting Script

 This is a simple script running python code, which connects to a database 
 and performs a series of sql queries on the postgresql dialect. All methods
 use the psycopg2 library.

#### popular_articles
 This method retrieves the three most popular articles.
 It connects to the database, performs the appropriate query, and returns
 a list of results. It's also structured around conditionals to catch 
 edge cases, and a for loop to format the output in english-friend structure.
 The following SQL command was used:
 
 ```
 """select articles.title, count(log.path) as views
    from articles
    left join log on substring(log.path, 10) = articles.slug
    where substring(log.path, 10) = articles.slug
    group by title
    order by views desc
    limit 3;"""
 ```

#### popular_authors
 This method is very similar to the first, but it retrieves the three most 
 popular authors by article views. The following SQL command was used:
 
 ```
 """select authors.name as auth_name, count(log.path) as views
    from articles
    left join log on substring(log.path, 10) = articles.slug
    right join authors on articles.author = authors.id
    where substring(log.path, 10) = articles.slug
    group by auth_name
    order by views desc;"""
 ```

#### error_days
 This method returns the days when the request error rate was above 1%.
 It is very similar to the previous two functions, but its sql query is a bit 
 more complex. The following SQL command was used:
 
 ```
 """select to_char(nums.day, 'Month dd, YYYY'),
    (nums.num*1.0/alls.all)*100 as percent
    from (select cast(time as date) as day, count(*) as num
            from log where status != '200 OK' group by day) as nums
    join (select cast(time as date) as day, count(*) as all
            from log group by day) as alls
    on nums.day = alls.day
    where (nums.num*1.0/alls.all)*100 > 1.0
    group by nums.day, percent
    order by percent desc;"""
 ```

#### Installation

 To run this script, you need to have a vm running on your OS, such as Vagrant. 
 After cd'ing into your vagrantfile location, make sure the vm is running with the

```
vagrant up
```

 command. Then log in with 

```
vagrant ssh
```
 Then download the 
 [database setup](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
 Retrieve the newsdata.sql file and put it in the same directory as your vagrantfile.
 Then from the cl, run:

```
psql -d news -f newsdata.sql
```

 Then run

```
python data_report.py
```

 This should produce results similar to the snippets in the example.txt file.
