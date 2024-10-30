import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import logging
from doubaiai import generate_content  # ����AIģ��
from toutiao_api import post_article   # ͷ��APIģ��

# ������־
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   filename='news_bot.log')

class NewsCollector:
    def __init__(self):
        self.keywords = ["����ս��", "�ڿ���", "����˹", "�ж���ͻ", "��ɫ��", "��ɳ"]
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
            
            # ��Բ�ͬԴ�����Ӧ�Ľ����߼�
            # ... ��������Դ�Ľ�������
            
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
            time.sleep(2)  # �����������
        return all_news

def main():
    try:
        # �ռ�����
        collector = NewsCollector()
        news_items = collector.collect_all_news()
        
        if not news_items:
            logging.warning("No relevant news found")
            return
            
        # ׼����ʾ��
        prompt = f"""
        �����������������һƪ�����������������£��ص��ע����ս�����ж���ͻ��
        {json.dumps(news_items, ensure_ascii=False)}
        Ҫ��
        1. ������Ҫ�б���
        2. ����Ҫ�͹۹���
        3. �ֶ�������ͬ�¼�
        4. ������1000������
        """
        
        # ʹ�ö���AI��������
        article = generate_content(prompt)
        
        # ������ͷ��
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
