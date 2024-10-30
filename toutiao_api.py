import requests
import json
import os

def post_article(article):
    try:
        # ͷ��API����
        API_KEY = os.getenv('TOUTIAO_API_KEY')
        url = "https://api.toutiao.com/article/publish"  # ʾ��API��ַ
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # �������±��������
        lines = article.split('\n')
        title = lines[0].strip()
        content = '\n'.join(lines[1:]).strip()
        
        data = {
            "title": title,
            "content": content,
            "article_type": 1,  # ��������
            "category_id": "news"  # ���·���
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.status_code == 200
        
    except Exception as e:
        logging.error(f"Error posting article: {str(e)}")
        return False
