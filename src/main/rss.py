import feedparser

# List of RSS feed URLs
rss_urls = [
    'https://www.cisa.gov/cybersecurity-advisories/all.xml',
    'https://www.us-cert.gov/ncas/current-activity.xml'
    ' https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml',
   
]

# Iterate through the list of feed URLs
for rss_url in rss_urls:
    feed = feedparser.parse(rss_url)
    
    print("RSS Feed:", rss_url)
    
    for entry in feed.entries:
        print("Title:", entry.title)
        print("Link:", entry.link)
        print()
