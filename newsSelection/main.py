import sqlite3

def record(username, news_id):
    conn = sqlite3.connect('./../userNews.db')
    cursor = conn.cursor() 
    cursor.execute(f"INSERT INTO Viewed VALUES ('{username}', '{news_id}')")
    conn.commit()   
    conn.close()
    selection(username)

def selection(username, topics):
    conn = sqlite3.connect('./../userNews.db')
    cursor = conn.cursor() 
    conn.execute(f"DELETE from Interests where username = '{username}'")
    for topic in topics:
        cursor.execute(f"INSERT INTO Interests VALUES ('{username}', '{topic}')")
    conn.commit()   
    conn.close()


"""CREATE TABLE Viewed
(username TEXT NOT NULL,
newsId TEXT NOT NULL);"""


"""CREATE TABLE Interests
(username TEXT NOT NULL,
interest TEXT NOT NULL);"""

if __name__ == "__main__":
    selection("ahmadi")