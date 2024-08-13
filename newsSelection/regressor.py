from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from hazm import Normalizer
import sqlite3
import pickle
import time


# فرض کنید داده‌های ما به شکل زیر هستند:
# texts = ["متن اول", "متن دوم", ...]
# scores = [0.5, 0.7, ...]

def regression():
    conn = sqlite3.connect('./../userNews.db')  
    usernames = list(conn.execute("SELECT username from Viewed"))
    usernames = list(map(lambda x: x[0], usernames))
    usernames = list(set(usernames))
    normalizer = Normalizer()
    vectorizer = TfidfVectorizer()
    for username in usernames:
        conn = sqlite3.connect('./../userNews.db')  
        textIds, scores = [], []
        stars = list(conn.execute(f"SELECT star from Viewed where username = '{username}'"))
        newsIds = list(conn.execute(f"SELECT newsId from Viewed where username = '{username}'"))
        isTrained = list(conn.execute(f"SELECT isTrained from Viewed where username = '{username}'"))
        isTrained = list(filter(lambda x: x[0]==0, isTrained))
        if len(isTrained) == 0:
            print(f"{username} doesn't need to be the trained again!")
            continue
        else:
            conn.execute(f"UPDATE Viewed SET isTrained = 1 where username = '{username}'")
        stars = list(map(lambda x: x[0], stars))
        newsIds = list(map(lambda x: x[0], newsIds))
        for i in range(len(newsIds)):
            f = True
            id = newsIds[i]
            for j in range(i+1, len(newsIds)):
                if id == newsIds[j]:
                    f = False
                    break
            if f:
                textIds.append(id)
                scores.append(stars[i])
        texts = []
        conn.commit()
        conn.close()
        conn = sqlite3.connect('./../news.db')
        i = 0
        for id in textIds:
            i += 1
            title = list(conn.execute(f"SELECT title from News where id = '{id}'"))
            abstract = list(conn.execute(f"SELECT abstract from News where id = '{id}'"))
            try:
                abstract = abstract[0][0]
            except:
                scores.pop(i)
                continue
            title = title[0][0]
            text = abstract
            texts.append(text)

        # نرمالایز کردن متن‌ها با استفاده از hazm
        normalized_texts = [normalizer.normalize(text) for text in texts]

        # تبدیل متن‌ها به ویژگی‌های عددی با استفاده از TF-IDF
        X = vectorizer.fit_transform(normalized_texts)

        # تقسیم داده‌ها به دو بخش آموزش و تست
        X_train, X_test, y_train, y_test = train_test_split(X, scores, test_size=0.2, random_state=42)

        # ساخت مدل MLPRegressor
        model = MLPRegressor(hidden_layer_sizes=(100,), max_iter=500, random_state=42)
        model.fit(X_train, y_train)

        # پیش‌بینی روی داده‌های تست
        y_pred = model.predict(X_test)

        # ارزیابی مدل
        mse = mean_squared_error(y_test, y_pred)
        print(f"{username} Mean Squared Error: {mse}")

        filename = f"../pickles/{username}_regressor.pkl"

        with open(filename, 'wb') as f:
            pickle.dump(model, f)

        filename = f"../pickles/{username}_vectorizer.pkl"

        with open(filename, 'wb') as f:
            pickle.dump(vectorizer, f)


        # with open(filename, 'rb') as f:
        #     model = pickle.load(f)
        
        # new_text = "این یک متن جدید است"
        # new_text_normalized = normalizer.normalize(new_text)
        # new_text_vectorized = vectorizer.transform([new_text_normalized])
        # predicted_score = model.predict(new_text_vectorized)
        # print(f"Predicted Score: {predicted_score[0]}")

if __name__ == "__main__":
    while True:
        print(u"\033[92mRegressor Is Running!\033[0m")
        regression()
        print(u"\033[95mEnd Regression!\033[0m")
        time.sleep(120)