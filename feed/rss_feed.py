from flask import Flask, render_template_string
from threading import Timer
import feedparser
from datetime import datetime

app = Flask(__name__)

# 이전에 발견된 최신 제목을 저장할 딕셔너리
latest_titles = {}

# RSS 피드 업데이트 주기 (초)
UPDATE_INTERVAL = 30
# 최대 메시지 수
MAX_MESSAGES = 200

feed_urls = [
    'https://www.yonhapnewstv.co.kr/browse/feed/',
    'https://biz.heraldcorp.com/common_prog/rssdisp.php?ct=010000000000.xml',
    'https://www.mk.co.kr/rss/30000001/',
    'https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml',
    'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114',
    'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362'
    # 다른 RSS 피드 URL을 여기에 추가할 수 있습니다.
]

def update_feeds():
    global latest_titles
    global feed_messages

    new_entries = []

    for url in feed_urls:
        feed = feedparser.parse(url)
        channel_title = feed.feed.get('title', '알 수 없는 채널')

        entries = [(entry.title, entry.link) for entry in feed.entries[:10]]
        updated_entries = [(title, link) for title, link in entries if (title, link) not in latest_titles.get(url, set())]

        if updated_entries:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for title, link in updated_entries:
                message = f"{current_time} - '{channel_title}': <a href=\"{link}\" target=\"_blank\">{title}</a><br>"
                new_entries.append(message)
            latest_titles[url] = set(entries)

    if new_entries:
        feed_messages = new_entries + feed_messages
        # 최대 메시지 수를 초과하면 오래된 메시지 삭제
        if len(feed_messages) > MAX_MESSAGES:
            feed_messages = feed_messages[:MAX_MESSAGES]

    Timer(UPDATE_INTERVAL, update_feeds).start()

# 초기 피드 메시지 리스트
feed_messages = []

# 피드 업데이트 시작
update_feeds()

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string("""
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>RSS 피드</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body {
        padding: 20px;
      }
      .feed-message {
        padding: 10px;
        border-bottom: 1px solid #ddd;
      }
      .feed-message:last-child {
        border-bottom: none;
      }
      .update-time {
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 12px;
        color: #888;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h3 class="my-4">RSS 피드</h3>
      <div id="update-time" class="update-time">마지막 업데이트: {{ current_time }}</div>
      <div id="feed-container" class="list-group">
        {% for message in feed_messages %}
          <div class="feed-message list-group-item">{{ message|safe }}</div>
        {% endfor %}
      </div>
    </div>
    <script>
      document.addEventListener("DOMContentLoaded", function(event) {
        // 10초마다 페이지를 새로 고침
        setInterval(function() {
          window.location.reload();
        }, 10000); // 10초마다 새로 고침
      });
    </script>
  </body>
</html>
    """, feed_messages=feed_messages, current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
