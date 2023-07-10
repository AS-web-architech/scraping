# import json
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# }

# urls = [
#     'https://www.carrefourksa.com/mafsau/en/pickles/pickles-bolieve-egypt/p/272256',
#     'https://www.carrefourksa.com/mafsau/en/smocked-roasted-meat/smoked-chicken-breast-alfolla/p/528783',
#     'https://www.carrefourksa.com/mafsau/en/smocked-roasted-meat/smoked-turkey-breast-americana/p/120886',
#     'https://www.carrefourksa.com/mafsau/en/beef/mortadella-beef-plain-low-fat-bibi/p/510151',
#     'https://www.carrefourksa.com/mafsau/en/olives/olive-grilled/p/638743'
# ]

# product_data_list = []
# with open('result.txt', 'w', encoding='utf-8') as file:
#     for url in urls:
#         response = requests.get(url, headers=headers)
        
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "html.parser")
#             script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            
#             if script_tag is not None:
#                 json_blob = json.loads(script_tag.contents[0])
#                 product_data = json_blob["props"]["initialProps"]["pageProps"]["initialData"]["products"]
                
#                 for product in product_data:
#                     name_ar = product.get('name_ar')  # Access the "name_ar" attribute
#                     status = product.get('status')  # Access the "name_ar" attribute
#                     quantity = product.get('quantity')  # Access the "name_ar" attribute
#                     price = product.get('name_ar')  # Access the "name_ar" attribute

#                     if name_ar:
#                         name_ar = name_ar.replace('\u0638', '?')
#                         product['name_ar'] = name_ar
#                     if status:
#                         status = status.replace('\u0638', '?')
#                         product['status'] = status
#                     if quantity:
#                         quantity = quantity.replace('\u0638', '?')
#                         product['quantity'] = quantity
#                     if price:
#                         price = price.replace('\u0638', '?')
#                         product['price'] = price
                    

#                     # Write the keys and values to the file
#                     for key, value in product.items():
#                         file.write(f'{key}: {value}\n')
                    
#                     product_data_list.append(product)

# # Create a DataFrame from the product data
# df = pd.DataFrame(product_data_list)

# # Convert DataFrame to Excel format
# df.to_excel('result.xlsx', index=False)
import json
import sys
from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
url = 'https://www.carrefourksa.com/mafsau/en/pickles/pickles-bolieve-egypt/p/272256'

response = requests.get(url, headers=headers)
print(response)
soup = BeautifulSoup(response.text, 'html.parser')
res = soup.find("script", {"id": "__NEXT_DATA__"})

with open('return.txt', 'w', encoding='utf-8') as file:
    file.write(str(res))

try:
    json_data = json.loads(res.contents[0])
    product_data = json_data["props"]["initialProps"]["pageProps"]["initialData"]["products"]

    for product in product_data:
        product_string = str(product)  # Convert the product dictionary to a string
        if 'name_ar' in product_string:
            start_index = product_string.find('name_ar') + len('name_ar":')
            end_index = product_string.find(',', start_index)
            name_ar = product_string[start_index:end_index].strip('"')
            print(name_ar.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
        if 'value' in product_string:
            start_index = product_string.find('value') + len('value":')
            end_index = product_string.find(',', start_index)
            value = product_string[start_index:end_index].strip('"')
            print(value.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
        if 'title' in product_string:
            start_index = product_string.find('title') + len('title":')
            end_index = product_string.find(',', start_index)
            title = product_string[start_index:end_index].strip('"')
            print(title.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
        else:
            print('name_ar key not found')

except json.JSONDecodeError:
    print("Failed to decode JSON data")
