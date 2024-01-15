import feedparser

def crawler():
    # feed = feedparser.parse("https://www.farsnews.ir/rss")
    feed = feedparser.parse("./rss")
    
    news = []

    for entry in feed.entries:
        theNews = {}
        theNews['id'] = entry.id
        theNews['id'] = theNews['id'][-14:]
        theNews['title'] = entry.title
        theNews['link'] = entry.link
        news.append(theNews)

    return news

news = crawler()

print(news)