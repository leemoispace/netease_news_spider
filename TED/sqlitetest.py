import sqlite3

#建立数据库
conn=sqlite3.connect("data/dbtest.db")
#建立cursor
cur=conn.cursor()
cur.execute('''CREATE TABLE TED
    (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        speaker CHAR,
        talk_name CHAR,
        talk_link TEXT,
        watch_times INT,
        place CHAR,
        length CHAR,
        month CHAR,
        brief_description TEXT,
        transcript TEXT,
        similar_topics TEXT
    );''')


conn.commit()

talk="aaa"
speaker="a"
talk_name="b"
watch_times=10
place="j"
length="k"
month="k"
brief_description="j"
transcript="\""
similar_topics="/"

cur.execute("INSERT INTO TED VALUES(null,?,?,?,null,null,null,null,null,null,null)",(speaker,talk_name,talk))
#watch_times,place,length,month,brief_description,transcript,similar_topics))
conn.commit()
