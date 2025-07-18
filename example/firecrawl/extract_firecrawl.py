# firecrawl_scraper.py
import json
import requests
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime




BASE_API_KEY = "fc-fc31e05397b04cf3aab96fb9d2ef27b1"
BASE_URL = "https://news.ycombinator.com/"


class NewsItem(BaseModel):
    title: str = Field(description="The title of the news item")
    source_url: str = Field(description="The URL of the news item")
    author: str = Field(
        description="The URL of the post author's profile concatenated with the base URL."
    )
    rank: str = Field(description="The rank of the news item")
    upvotes: str = Field(description="The number of upvotes of the news item")
    date: str = Field(description="The date of the news item.")


class NewsData(BaseModel):
    news_items: List[NewsItem]



url = "https://api.firecrawl.dev/v1/extract"

payload = {
    "urls": [BASE_URL],
    "formats": ["json"],
    "schema": NewsData.model_json_schema()
}

headers = {
    "Authorization": "Bearer fc-fc31e05397b04cf3aab96fb9d2ef27b1",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)



def save_firecrawl_news_data():
    """
    Save the scraped news data to a JSON file with the current date in the filename.
    """
    # Get the data
    data = response.json()
    
    # 打印数据结构以便调试
    print("Data type:", type(data))
    print("Data attributes:", dir(data))
    
    # Format current date for filename
    date_str = datetime.now().strftime("%Y_%m_%d_%H_%M")
    filename = f"firecrawl_hacker_news_data_{date_str}.json"

    # 尝试不同的数据访问方式 (for /v1/extract endpoint)
    try:
        # Extract端点的响应结构分析
        if isinstance(data, dict):
            # 可能的响应结构：
            # 1. {"success": true, "data": [{"extract": {...}}, ...]}
            # 2. {"success": true, "data": {"extract": {...}}}
            # 3. {"extract": {...}}
            
            if 'data' in data:
                extract_data = data['data']
                if isinstance(extract_data, list) and extract_data:
                    # 如果data是数组，取第一个元素
                    first_item = extract_data[0]
                    news_data = first_item.get('extract', {}).get('news_items', [])
                elif isinstance(extract_data, dict):
                    news_data = extract_data.get('extract', {}).get('news_items', [])
                else:
                    news_data = []
            elif 'extract' in data:
                news_data = data['extract'].get('news_items', [])
            else:
                news_data = data.get('news_items', [])
        # 如果是SDK响应对象
        elif hasattr(data, 'extract'):
            news_data = data.extract.get('news_items', [])
        # 方式3: 转换为字典
        else:
            data_dict = data.model_dump() if hasattr(data, 'model_dump') else dict(data)
            news_data = data_dict.get('extract', {}).get('news_items', [])
            
        # Save the news items to JSON file
        with open(filename, "w") as f:
            json.dump(news_data, f, indent=4)

        print(f"{datetime.now()}: Successfully saved the news data.")
        
    except Exception as e:
        print(f"Error accessing data: {e}")
        print("Raw data:", data)

if __name__ == "__main__":
    save_firecrawl_news_data()


