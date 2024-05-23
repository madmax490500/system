from flask import Flask, render_template_string
from threading import Timer, Lock
import feedparser
from datetime import datetime

app = Flask(__name__)

# 이전에 발견된 최신 제목을 저장할 딕셔너리
latest_titles = {}

# RSS 피드 업데이트 주기 (10초)
UPDATE_INTERVAL = 10

feed_urls = [
    'https://www.yonhapnewstv.co.kr/browse/feed/',
    'https://biz.heraldcorp.com/common_prog/rssdisp.php?ct=010000000000.xml',
    'https://www.mk.co.kr/rss/30000001/',
    'https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml',
    # 다른 RSS 피드 URL을 여기에 추가할 수 있습니다.
]

# Mutex Lock 생성
update_lock = Lock()

def update_feeds():
    global latest_titles

    new_entries = []

    # Lock을 획득하여 다른 스레드가 update_feeds 함수를 호출하지 못하도록 함
    with update_lock:
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
            global feed_messages
            feed_messages.extend(new_entries)

    # Timer 객체가 실행 중이 아닌 경우에만 새로운 Timer 객체 생성
    if not hasattr(update_feeds, "timer") or not update_feeds.timer.is_alive():
        update_feeds.timer = Timer(UPDATE_INTERVAL, update_feeds)
        update_feeds.timer.start()

# 초기 피드 메시지 리스트
feed_messages = []

# 피드 업데이트 시작
update_feeds()

@app.route('/')
def home():
    return render_template_string("""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>RSS feed checker</title>
        <!-- Bootstrap CSS -->
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <script>
          // 페이지를 1분마다 새로고침하는 함수
          setTimeout(function(){
             window.location.reload(1);
          }, 60000);  // 60000 밀리초 = 1분
        </script>
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
        </style>
      </head>
      <body>
        <div class="container">
          <h3 class="my-4">RSS feed checker</h3>
          <div id="feed-container" class="list-group">
            {% for message in feed_messages %}
              <div class="feed-message list-group-item">{{ message|safe }}</div>
            {% endfor %}
          </div>
        </div>
      </body>
    </html>
    """, feed_messages=feed_messages)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)

