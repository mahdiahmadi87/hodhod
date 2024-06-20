import sqlite3

def record(username, news_id, n):
    conn = sqlite3.connect('./../userNews.db')
    cursor = conn.cursor() 
    cursor.execute(f"INSERT INTO Viewed VALUES ('{username}', '{news_id}', {n})")
    conn.commit()   
    conn.close()

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
newsId TEXT NOT NULL,
star INTEGER NOT NULL);"""

"""CREATE TABLE Interests
(username TEXT NOT NULL,
interest TEXT NOT NULL);"""

if __name__ == "__main__":
    selection("ahmadi")