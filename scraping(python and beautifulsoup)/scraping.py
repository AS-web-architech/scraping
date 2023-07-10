import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

df = pd.read_excel('myurls.xlsx')
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
            product_list = page_data.get("props", {}).get("initialProps", {}).get("pageProps", {}).get("initialData", {}).get("products", [])

            for product in product_list:
                extracted_data = {}
                # Extract the desired information from the product dictionary
                if 'name_ar' in product:
                    extracted_data['Name_Ar'] = product['name_ar']
                if 'title' in product:
                    extracted_data['Name_En'] = product['title']
                if 'attributes' in product and 'brandName' in product['attributes']:
                    extracted_data['ProductManufacturer'] = product['attributes']['brandName']
                if 'attributes' in product and 'barCodes' in product['attributes']:
                    extracted_data['BarCodes'] = product['attributes']['barCodes']

                if 'offers' in product and product['offers']:
                    store_data = product['offers'][0]["stores"][0]["storeData"]
                    if 'status' in store_data:
                        extracted_data['Status'] = store_data['status']
                    if 'quantity' in store_data:
                        extracted_data['Quantity'] = store_data['quantity']
                
                if 'categories' in product and product['categories']:
                    product_category = product['categories'][0]
                    if 'name' in product_category:
                        extracted_data['Category'] = product_category['name']
                
                if 'offers' in product and product['offers']:
                   product_price = product['offers'][0]['stores'][0]['price']
                   if product_price and 'original' in product_price:
                       extracted_data['Price'] = product_price['original']['value']
                
                if 'media' in product and product['media']:
                    product_image = product['media'][0]
                    if 'url' in product_image:
                        extracted_data['ProductImage'] = product_image['url']
                
                product_data_list.append(extracted_data)

        except json.JSONDecodeError:
            print("Failed to decode JSON data")
    else:
        print("Script tag with ID '__NEXT_DATA__' not found")

# Create a DataFrame from the scraped data
df = pd.DataFrame(product_data_list)

# Convert DataFrame to Excel format
df.to_excel('output1.xlsx', index=False)
