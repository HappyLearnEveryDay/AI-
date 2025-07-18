import requests
import re
import json
from datetime import datetime

url = "https://api.firecrawl.dev/v1/scrape"

payload = {
    "url": "https://www.qidian.com/chapter/1010868264/516668668/",
    "formats": ["markdown"],
    "onlyMainContent": True,
}
headers = {
    "Authorization": "Bearer fc-fc31e05397b04cf3aab96fb9d2ef27b1",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)

# Save the response content to a markdown file and extract links
if response.status_code == 200:
    try:
        # Parse the JSON response
        data = response.json()
        
        # Extract markdown content
        markdown_content = data.get('data', {}).get('markdown', '')
        
        if markdown_content:
            # Generate filename with current timestamp
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            filename = f"scraped_content_{timestamp}.md"
            
            # Save to markdown file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Content successfully saved to {filename}")
            
            # Extract chapter links
            if markdown_content:
                # Save links to JSON file
                links_filename = f"extracted_links_{timestamp}.json"
                links_data = {
                    "timestamp": timestamp,
                    "source_url": payload["url"],
                    "total_links": len(markdown_content),
                    "links": markdown_content
                }
                
                with open(links_filename, 'w', encoding='utf-8') as f:
                    json.dump(links_data, f, ensure_ascii=False, indent=2)
                
                print(f"Found {len(markdown_content)} chapter links")
                print(f"Links saved to {links_filename}")
                
                # Print first few links as preview
                print("\nPreview of extracted links:")
                for i, link in enumerate(markdown_content[:5]):
                    print(f"{i+1}. {link}")
                if len(markdown_content) > 5:
                    print(f"... and {len(markdown_content) - 5} more links")
                
            else:
                print("No chapter links found in the content")
                
        else:
            print("No markdown content found in response")
            
    except json.JSONDecodeError:
        print("Failed to parse JSON response")
    except Exception as e:
        print(f"Error saving file: {e}")
else:
    print(f"Request failed with status code: {response.status_code}")

