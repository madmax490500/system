import feedparser
import time

URL = "https://vitta.tistory.com/rss"
RSS_FEED = feedparser.parse(URL)
MAX_POST = 5

# 디버깅: 피드 파싱 확인
if RSS_FEED.bozo:
    print("Error parsing feed:", RSS_FEED.bozo_exception)
else:
    print("Feed parsed successfully")

# 디버깅: 피드 엔트리 확인
if 'entries' in RSS_FEED:
    print(f"Number of entries: {len(RSS_FEED['entries'])}")
else:
    print("No entries found in the feed")

markdown_text = """
## ✅ Latest Blog Posts

"""  # list of blog posts will be appended here

for idx, feed in enumerate(RSS_FEED.get('entries', [])):
    if idx >= MAX_POST:
        break
    else:
        feed_date = feed.get('published_parsed')
        if feed_date:
            formatted_date = time.strftime('%Y/%m/%d', feed_date)
        else:
            formatted_date = "Unknown date"
        
        title = feed.get('title', 'No title')
        link = feed.get('link', '#')
        
        # 디버깅: 각 피드 항목 확인
        print(f"Post {idx + 1}: {formatted_date} - {title}")

        markdown_text += f"[{formatted_date} - {title}]({link}) <br/>\n"

# 디버깅: 최종 마크다운 내용 확인
print("Generated markdown text:")
print(markdown_text)

with open("README.md", mode="w", encoding="utf-8") as f:
    f.write(markdown_text)
    # 디버깅: 파일 작성 확인
    print("README.md file has been written.")
