import feedparser

def crawler():
    feed = feedparser.parse("https://www.tasnimnews.com/fa/rss/feed/0/8/0/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%AE%D8%A8%D8%B1%D9%87%D8%A7%DB%8C-%D8%B1%D9%88%D8%B2")
    # feed = feedparser.parse("./rss")
    
    news = []

    for entry in feed.entries:
        theNews = {}
        theNews['id'] = entry.id
        theNews['id'] = theNews['id'][-7:]
        theNews['title'] = entry.title
        theNews['link'] = entry.link
        news.append(theNews)

    return news

news = crawler()

print(news)