import sqlite3

def record(username, news_id):
    conn = sqlite3.connect('./../userNews.db')
    cursor = conn.cursor() 
    cursor.execute(f"INSERT INTO Viewed VALUES ('{username}', '{news_id}')")
    conn.commit()   
    conn.close()
    selection(username)

def selection(username):
    conn = sqlite3.connect('./../userNews.db')
    viewed = list(conn.execute(f"SELECT newsId from Viewed where username = '{username}'"))
    viewed = list(map(lambda x: x[0], viewed))
    conn.close()

    conn = sqlite3.connect('./../news.db')
    topics = []
    for newsId in viewed:
        newsTopic = list(conn.execute(f"SELECT topic from TasnimNews where id = {newsId}"))[0][0]
        newsTopic = newsTopic.split("|")
        topics = topics + newsTopic
    conn.close()

    conn = sqlite3.connect('./../userNews.db')
    cursor = conn.cursor() 

    lastTopics = list(conn.execute(f"SELECT interest from Interests where username = '{username}'"))
    lastTopics = list(map(lambda x: x[0], lastTopics))
    topics = topics + lastTopics
    topics = list(set(topics))
    print(topics)
    conn.execute(f"DELETE from Interests where username = '{username}'")
    for topic in topics:
        cursor.execute(f"INSERT INTO Interests VALUES ('{username}', '{topic}')")
    conn.commit()   
    conn.close()

    return True


"""CREATE TABLE Viewed
(username TEXT NOT NULL,
newsId TEXT NOT NULL);"""


"""CREATE TABLE Interests
(username TEXT NOT NULL,
interest TEXT NOT NULL);"""

if __name__ == "__main__":
    selection("ahmadi")