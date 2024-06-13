import sqlite3

def record(username, news_id):
    conn = sqlite3.connect('./../userNews.db')
    cursor = conn.cursor() 
    cursor.execute(f"INSERT INTO Users VALUES ('{username}', '{news_id}')")
    conn.commit()   
    conn.close()

def selection(l:list):
    return True

"""CREATE TABLE Users
(username TEXT NOT NULL,
newsId TEXT NOT NULL);"""


