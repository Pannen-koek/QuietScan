import feedparser
import html

# List of RSS feed URLs
rss_urls = [
    'https://www.cisa.gov/cybersecurity-advisories/all.xml',
    'https://www.us-cert.gov/ncas/current-activity.xml'
    'https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml',
    'https://krebsonsecurity.com/feed/',
    'https://feeds.feedburner.com/TheHackersNews?format=xml',
   
]

# Iterate through the list of feed URLs
for rss_url in rss_urls:
    feed = feedparser.parse(rss_url)
    
    print("RSS Feed:", rss_url)

    for entry in feed.entries:
        title = html.unescape(entry.title)
        link = html.unescape(entry.link)

    for entry in feed.entries:
        print("Title:", html.escape(title))
        print("Link:", link)
        print()
