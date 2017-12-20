#!/usr/bin/env python3

import psycopg2


def most_popular():
    # connect to database
    conn = psycopg2.connect(database='news')
    # retrieve cursor
    c = conn.cursor()
    # set sql statement
    sql = """select articles.title, count(log.path) as views
                from articles
                left join log on substring(log.path, 10) = articles.slug
                where substring(log.path, 10) = articles.slug
                group by title
                order by views desc
                limit 3;"""
    # execute query
    c.execute(sql)
    # retrieve results in a list
    rows = c.fetchall()
    # if list is empty, return
    if len(rows) == 0:
        conn.close()
        return
    conn.close()
    # iterate through list, append formatted results
    for row in rows:
        print ("".join(row[0] + ' - ' + str(row[1]) + ' views\n'))
    return


def popular_authors():
    # connect to database
    conn = psycopg2.connect(database='news')
    # retrieve cursor
    c = conn.cursor()
    # set sql statement
    sql = """select authors.name as auth_name, count(log.path) as views
                from articles
                left join log on substring(log.path, 10) = articles.slug
                right join authors on articles.author = authors.id
                where substring(log.path, 10) = articles.slug
                group by auth_name
                order by views desc;"""
    # execute query
    c.execute(sql)
    # retrieve results in a list
    rows = c.fetchall()
    # if list is empty, return
    if len(rows) == 0:
        conn.close()
        return
    conn.close()
    # iterate through list, append formatted results
    for row in rows:
        print ("".join(row[0] + ' - ' + str(row[1]) + ' views\n'))
    return


def error_days():
    # connect to database
    conn = psycopg2.connect(database='news')
    # retrieve cursor
    c = conn.cursor()
    # set sql statement
    sql = """select to_char(nums.day, 'Month dd, YYYY'),
                (nums.num*1.0/alls.all)*100 as percent
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
    # if list is empty, return
    if len(rows) == 0:
        conn.close()
        return
    # otherwise iterate through list, append formatted results
    if len(rows) > 1:
        for row in rows:
            print ("".join(row[0] + " - " +
                    str(round(row[1], 1)) + "% errors\n"))
        conn.close()
        return
    else:
        conn.close()
        print (rows[0] + " - " + str(round(row[1], 1)) + "% errors")
        return
