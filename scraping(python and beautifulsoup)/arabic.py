import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

df = pd.read_excel('arabic urls.xlsx')
urls_column = 'URLS'

product_data_list = []

# Extract the URLs from the specified column
urls = df[urls_column].tolist()
for url in urls:
    response = requests.get(url, headers=headers)
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    extracted_data_tag = soup.find("script", {"id": "__NEXT_DATA__"})

    if extracted_data_tag:
        extracted_data = extracted_data_tag.text  # Extract the text content from the Tag object

        try:
            page_data = json.loads(extracted_data)
            product_list = page_data["props"]["initialProps"]["pageProps"]["initialData"]["products"]

            for product in product_list:
                extracted_data = {}
                # Extract the desired information from the product dictionary
                
                if 'title' in product:
                    extracted_data['Name_Ar'] = product['title']
                
            
                product_data_list.append(extracted_data)

        except json.JSONDecodeError:
            print("Failed to decode JSON data")
    else:
        print("Script tag with ID '__NEXT_DATA__' not found")

# Create a DataFrame from the scraped data
df = pd.DataFrame(product_data_list)

# Convert DataFrame to Excel format
df.to_excel('output1.xlsx', index=False)
