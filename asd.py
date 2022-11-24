import psycopg2

con= psycopg2.connect(
    database='exampledb',
    user='docker',
    password='docker',
    host='192.168.1.127',port='4000')
with con.cursor() as cur:
    cur.execute('SELECT * FROM exampledb')
    for c in cur.fetchall():
        print(c)