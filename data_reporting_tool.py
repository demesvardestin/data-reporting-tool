# Data Reporting Tool
# Demesvar Destin

import psycopg2

def most_popular(database='news'):
    # connect to database
    conn = psycopg2.connect(database)
    # retrieve cursor
    c = conn.cursor()
    # set sql statement
    sql = """select articles.title, count(log.path) as views 
                from articles left join log on substring(log.path, 10) = articles.slug 
                where substring(log.path, 10) = articles.slug 
                group by title 
                order by views desc 
                limit 3;"""
    # execute query
    c.execute(sql)
    # retrieve results in a list
    rows = c.fetchall()
    articles = []
    # if list is empty, return
    if len(rows) == 0:
        conn.close()
        return
    # iterate through list, append formatted results
    for row in rows:
        articles.append("".join(row[0]+ ' - ' + str(row[1]) + ' views\n'))
    # close db connection
    conn.close()
    return articles
    
def popular_authors(database='news'):
    # connect to database
    conn = psycopg2.connect(database)
    # retrieve cursor
    c = conn.cursor()
    # set sql statement
    sql = """select authors.name as auth_name, count(log.path) as views 
                from articles left join log on substring(log.path, 10) = articles.slug 
                right join authors on articles.author = authors.id 
                where substring(log.path, 10) = articles.slug 
                group by auth_name 
                order by views desc;"""
    # execute query
    c.execute(sql)
    # retrieve results in a list
    rows = c.fetchall()
    authors = []
    # if list is empty, return
    if len(rows) == 0:
        conn.close()
        return
    # iterate through list, append formatted results
    for row in rows:
        authors.append("".join(row[0] + ' - ' + str(row[1]) + ' views\n'))
    # close db connection
    conn.close()
    return authors
    
def error_days(database='news'):
    # connect to database
    conn = psycopg2.connect(database)
    # retrieve cursor
    c = conn.cursor()
    # set sql statement
    sql = """select nums.day, (nums.num*1.0/alls.all)*100 as percent 
                from (select cast(time as date) as day, count(*) as num 
                        from log where status != '200 OK' group by day) as nums 
                join (select cast(time as date) as day, count(*) as all 
                        from log group by day) as alls 
                on nums.day = alls.day 
                where (nums.num*1.0/alls.all)*100 > 1.0 
                group by nums.day, percent 
                order by percent desc;"""
    # execute query
    c.execute(sql)
    # retrieve results in a list
    rows = c.fetchall()
    days = []
    # if list is empty, return
    if len(rows) == 0:
        conn.close()
        return
    # otherwise iterate through list, append formatted results
    if len(rows) > 1:
        for row in rows:
            days.append("".join(row[0] + " - " + str(row[1])[:3] + "% errors\n"))
        conn.close()
        return days
    else:
        conn.close()
        day = rows[0] + " - " + str(row[1])[:3] + "% errors"
        return day