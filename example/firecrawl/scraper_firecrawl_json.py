# firecrawl_scraper.py
import json
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


BASE_API_KEY = "fc-661bf538e5f4461e9348685fd2516b16"
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


def get_firecrawl_news_data():
    app = FirecrawlApp(api_key=BASE_API_KEY)

    data = app.scrape_url(
        BASE_URL,
        formats=["extract"],
        extract={"schema": NewsData.model_json_schema()},
    )

    return data


def save_firecrawl_news_data():
    """
    Save the scraped news data to a JSON file with the current date in the filename.
    """
    # Get the data
    data = get_firecrawl_news_data()
    
    # 打印数据结构以便调试
    print("Data type:", type(data))
    print("Data attributes:", dir(data))
    
    # Format current date for filename
    date_str = datetime.now().strftime("%Y_%m_%d_%H_%M")
    filename = f"firecrawl_hacker_news_data_{date_str}.json"

    # 尝试不同的数据访问方式
    try:
        # 方式1: 如果是ScrapeResponse对象，尝试.extract属性
        if hasattr(data, 'extract'):
            news_data = data.extract.get('news_items', [])
        # 方式2: 如果有data属性
        elif hasattr(data, 'data'):
            news_data = data.data.get('extract', {}).get('news_items', [])
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