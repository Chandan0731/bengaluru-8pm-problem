import requests
import xml.etree.ElementTree as ET

# Public Google News RSS feed for Bengaluru traffic, rain, and KSRTC festival rush
url = "https://news.google.com/rss/search?q=Bengaluru+traffic+rain+OR+KSRTC+long+weekend&hl=en-IN&gl=IN&ceid=IN:en"
res = requests.get(url)
print("News RSS Status Code:", res.status_code)

if res.status_code == 200:
    root = ET.fromstring(res.content)
    items = root.findall(".//item")
    print(f"Articles fetched: {len(items)}\n")
    for item in items[:5]:
        title = item.find("title").text
        pub_date = item.find("pubDate").text
        print(f"- [{pub_date}] {title}")