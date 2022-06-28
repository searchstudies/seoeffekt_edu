from lib.sources import save_source

import sqlite3 as sl

def connect_to_db():
    connection = sl.connect('seo_effect.db', timeout=10, isolation_level=None)
    connection.execute('pragma journal_mode=wal')
    return connection

def close_connection_to_db(connection):
    connection.close()


urls = []

connection = connect_to_db()
cursor = connection.cursor()
data = cursor.execute("SELECT SOURCE.id, SOURCE.result_id, SEARCH_RESULT.url FROM SOURCE,SEARCH_RESULT WHERE SOURCE.result_id = SEARCH_RESULT.id AND SOURCE.PROGRESS=? ORDER BY RANDOM() LIMIT 50", (0,))
connection.commit()

for row in data:
    source_id = row[0]
    result_id = row[1]
    url = row[2]

    urls.append([source_id, url])

close_connection_to_db(connection)

for v in urls:
    connection = connect_to_db()
    cursor = connection.cursor()
    source_id = v[0]
    cursor.execute("UPDATE SOURCE SET progress =? WHERE id =?", (2,source_id,))
    connection.commit()
    close_connection_to_db(connection)


for v in urls:
    connection = connect_to_db()
    cursor = connection.cursor()
    source_id = v[0]
    url = v[1]
    source = save_source(url)
    print(source_id)
    cursor.execute("UPDATE SOURCE SET progress =?, source=? WHERE id =?", (1,source,source_id,))
    connection.commit()
    close_connection_to_db(connection)
