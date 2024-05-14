import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser
from PyQt5.QtCore import QTimer
import feedparser
from datetime import datetime

# 이전에 발견된 최신 제목을 저장할 딕셔너리
latest_titles = {}

class FeedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSS 피드 확인기")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)  # 링크를 클릭할 수 있도록 설정
        self.layout.addWidget(self.text_browser)
        self.setLayout(self.layout)

        # RSS 피드 업데이트 타이머 설정 (10초마다)
        self.feed_update_timer = QTimer(self)
        self.feed_update_timer.timeout.connect(self.update_feeds)
        self.feed_update_timer.start(10000)  # 10초마다

        # 초기 RSS 피드 업데이트
        self.update_feeds()

    def update_feeds(self):
        global latest_titles

        # 여러 개의 RSS 피드 URL 리스트
        feed_urls = [
            #'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114',
            'https://www.yonhapnewstv.co.kr/browse/feed/',
            'https://biz.heraldcorp.com/common_prog/rssdisp.php?ct=010000000000.xml',
            'https://www.mk.co.kr/rss/30000001/',
            'https://www.chosun.com/arc/outboundfeeds/rss/?outputType=xml',
            # 다른 RSS 피드 URL을 여기에 추가할 수 있습니다.
        ]

        # 각각의 피드 URL에 대해 업데이트를 확인
        for url in feed_urls:
            feed = feedparser.parse(url)
            channel_title = feed.feed.get('title', '알 수 없는 채널')

            new_entries = [(entry.title, entry.link) for entry in feed.entries[:10]]

            updated_entries = [(title, link) for title, link in new_entries if (title, link) not in latest_titles.get(url, set())]
            if updated_entries:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for title, link in updated_entries:
                    message = f"{current_time} - '{channel_title}': <a href=\"{link}\">{title}</a><br>"
                    self.text_browser.append(message)
                latest_titles[url] = set(new_entries)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FeedWindow()
    window.show()
    sys.exit(app.exec_())

