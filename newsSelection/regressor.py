from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from hazm import Normalizer
import sqlite3
import pickle
import os


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
        textIds, scores = [], []
        stars = list(conn.execute(f"SELECT star from Viewed where username = '{username}'"))
        newsIds = list(conn.execute(f"SELECT newsId from Viewed where username = '{username}'"))
        conn.close()
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
        conn = sqlite3.connect('./../news.db')
        for id in textIds:
            title = list(conn.execute(f"SELECT title from TasnimNews where id = '{id}'"))
            abstract = list(conn.execute(f"SELECT abstract from TasnimNews where id = '{id}'"))
            abstract = abstract[0][0]
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
    regression()