import feedparser
import time
import os

# Constants
URL = "https://vitta.tistory.com/rss"
MAX_POST = 5
README_FILE = "README.md"

# Parse the RSS feed
RSS_FEED = feedparser.parse(URL)

# Add the "Last Updated" section with the current date and time at the top
last_updated_text = f"**Last Updated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

# Start building the markdown content
new_markdown_text = last_updated_text + """
[![Python application](https://github.com/madmax490500/madmax490500/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/madmax490500/madmax490500/actions/workflows/main.yml)
### 시스템엔지니어가 사용하는 코드 저장소입니다.
### This repository use by System Engineer.
### 지속적인 목표 (The objective of devops)
* 서비스의 안정성을 유지하면서 변화를 최대한 수용한다.
* 시스템의 상태와 가용성을 꾸준히 모니터링 한다.
* 어떤 기능에 대해 문제가 발생하면 이에 대해 긴급 대응을 한다.
* 시스템의 변화를 추적하고 관리한다.
* 수요를 예측하고, 계획을 세운다.
* 이를 통해 서비스의 수용력을 확보하고, 효율성을 향상한다.
## ✅ Latest Blog Posts
"""
# Add feed entries to the markdown using bullet points
for idx, feed in enumerate(RSS_FEED['entries']):
    if idx >= MAX_POST:  # Include only up to MAX_POST entries
        break
    feed_date = feed['published_parsed']
    formatted_date = time.strftime('%Y/%m/%d', feed_date)
    new_markdown_text += f"- [{formatted_date} - {feed['title']}]({feed['link']})\n"

# Function to read the content of the existing README file
def read_existing_readme(file_path):
    if os.path.exists(file_path):
        with open(file_path, mode="r", encoding="utf-8") as f:
            return f.read()
    return ""

# Read the existing README.md content
existing_markdown_text = read_existing_readme(README_FILE)

# Compare and write to the README.md file
if new_markdown_text.strip() != existing_markdown_text.strip():
    with open(README_FILE, mode="w", encoding="utf-8") as f:
        f.write(new_markdown_text)
    print("README.md has been updated with new RSS feed entries.")
else:
    # If no changes, still update the "Last Updated" section at the top
    new_markdown_text = last_updated_text + existing_markdown_text.strip()
    with open(README_FILE, mode="w", encoding="utf-8") as f:
        f.write(new_markdown_text)
    print("No changes in RSS feed, but README.md 'Last Updated' timestamp has been refreshed.")