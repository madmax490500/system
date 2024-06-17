import feedparser, time

URL = "https://vitta.tistory.com/rss"
RSS_FEED = feedparser.parse(URL)
MAX_POST = 5

markdown_text = """
### 시스템엔지니어가 사용하는 코드 저장소입니다.
### This repository use by SRE.

### 지속적인 목표 (SRE 목표)
* 서비스의 안정성을 유지하면서 변화를 최대한 수용한다.
* 시스템의 상태와 가용성을 꾸준히 모니터링 한다.
* 어떤 기능에 대해 문제가 발생하면 이에 대해 긴급 대응을 한다.
* 시스템의 변화를 추적하고 관리한다.
* 수요를 예측하고, 계획을 세운다.
* 이를 통해 서비스의 수용력을 확보하고, 효율성을 향상한다.


## ✅ Latest Blog Posts 
"""  # list of blog posts will be appended here

for idx, feed in enumerate(RSS_FEED['entries']):
    if idx > MAX_POST:
        break
    else:
        feed_date = feed['published_parsed']
        markdown_text += f"[{time.strftime('%Y/%m/%d', feed_date)} - {feed['title']}]({feed['link']}) <br/>\n"
        
f = open("README.md", mode="w", encoding="utf-8")
f.write(markdown_text)
f.close()