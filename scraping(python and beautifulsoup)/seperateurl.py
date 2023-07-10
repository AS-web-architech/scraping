import re
import pandas as pd

df = pd.read_excel('seperateurls.xlsx')
urls_column = 'URLS'
urls = df[urls_column].tolist()

def extract_urls(urls):
    separated_urls = []

    for url in urls:
        index = url.find("en/")
        if index != -1:
            separated_url = url[index + 3:]
            separated_urls.append(separated_url)
        else:
            separated_urls.append("")

    return separated_urls

separated_urls = extract_urls(urls)

df = pd.DataFrame(separated_urls )

# Convert DataFrame to Excel format
df.to_excel('sepurlsoutput.xlsx', index=False)