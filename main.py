import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import logging
from doubaiai import generate_content  # 豆包AI模块
from toutiao_api import post_article   # 头条API模块

# 配置日志
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   filename='news_bot.log')

class NewsCollector:
    def __init__(self):
        self.keywords = ["俄乌战争", "乌克兰", "俄罗斯", "中东冲突", "以色列", "加沙"]
        self.news_sources = {
            'bbc': 'https://www.bbc.com/news/world',
            'cnn': 'https://edition.cnn.com/world',
            'reuters': 'https://www.reuters.com/world/',
            'xinhua': 'http://www.xinhuanet.com/world/',
            'cctv': 'https://news.cctv.com/world/'
        }
        
    def get_news(self, url, source):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_items = []
            
            if source == 'bbc':
                articles = soup.find_all('article')
                for article in articles:
                    title = article.find('h3')
                    if title and self._contains_keywords(title.text):
                        news_items.append({
                            'title': title.text.strip(),
                            'source': 'BBC'
                        })
            
            # 针对不同源添加相应的解析逻辑
            # ... 其他新闻源的解析代码
            
            return news_items
            
        except Exception as e:
            logging.error(f"Error scraping {source}: {str(e)}")
            return []

    def _contains_keywords(self, text):
        return any(keyword.lower() in text.lower() for keyword in self.keywords)

    def collect_all_news(self):
        all_news = []
        for source, url in self.news_sources.items():
            news = self.get_news(url, source)
            all_news.extend(news)
            time.sleep(2)  # 避免请求过快
        return all_news

def main():
    try:
        # 收集新闻
        collector = NewsCollector()
        news_items = collector.collect_all_news()
        
        if not news_items:
            logging.warning("No relevant news found")
            return
            
        # 准备提示词
        prompt = f"""
        请根据以下新闻生成一篇完整的新闻综述文章，重点关注俄乌战争和中东冲突：
        {json.dumps(news_items, ensure_ascii=False)}
        要求：
        1. 文章需要有标题
        2. 内容要客观公正
        3. 分段论述不同事件
        4. 字数在1000字左右
        """
        
        # 使用豆包AI生成文章
        article = generate_content(prompt)
        
        # 发布到头条
        if article:
            post_result = post_article(article)
            if post_result:
                logging.info("Article posted successfully")
            else:
                logging.error("Failed to post article")
        
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")

if __name__ == "__main__":
    main()
