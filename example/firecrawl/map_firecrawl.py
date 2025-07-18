
import requests

url = "https://api.firecrawl.dev/v1/map"

payload = {
    "url": "https://firecrawl.dev",
}
headers = {
    "Authorization": "Bearer fc-fc31e05397b04cf3aab96fb9d2ef27b1",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)

# Save the response to a markdown file
import json
from datetime import datetime

# Parse the response
response_data = response.json()

# Create filename with timestamp
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
filename = f"firecrawl_map_result_{timestamp}.md"

# Format the content as markdown
markdown_content = f"# Firecrawl Map Result\n\n"
markdown_content += f"**Generated at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
markdown_content += f"**URL:** {payload['url']}\n\n"
markdown_content += f"## Configuration\n\n"
markdown_content += f"```json\n{json.dumps(payload, indent=2)}\n```\n\n"
markdown_content += f"## Response\n\n"
markdown_content += f"```json\n{json.dumps(response_data, indent=2, ensure_ascii=False)}\n```\n"

# Write to file
with open(filename, 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print(f"Results saved to {filename}")


