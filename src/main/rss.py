import feedparser
import html
import customtkinter
import ttkbootstrap as tb

rss_url = 'https://krebsonsecurity.com/feed/'


# Iterate through the list of feed URLs

def getRSSFeed():
    rssEntries = []
    rssEntriesRef = 0
    feed = feedparser.parse(rss_url)

    # print("RSS Feed:", rss_url)

    for entry in feed.entries:
        title = html.unescape(entry.title)
        link = html.unescape(entry.link)
        savedTitle = html.escape(title)
        savedLink = link
        rssEntries.append([savedTitle, savedLink])
        rssEntriesRef = rssEntriesRef + 1

        # for savedTitle, savedLink in rssEntries:
        # print(savedTitle, savedLink)

    return rssEntries
