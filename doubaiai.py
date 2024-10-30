import requests
import json
import os

def generate_content(prompt):
    try:
        # 豆包AI的API配置
        API_KEY = os.getenv('DOUBAI_API_KEY')
        url = "https://api.doubai.com/v1/chat/completions"  # 示例API地址
        
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "doubai-text",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        return result['choices'][0]['message']['content']
        
    except Exception as e:
        logging.error(f"Error generating content: {str(e)}")
        return None
