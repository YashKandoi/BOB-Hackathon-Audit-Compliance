from urllib.parse import urlparse
import requests
import os

# def jina_website_content(url):
#     url = urlparse("https://r.jina.ai/" + url).geturl()
#     headers = {
#         'Accept': 'application/json',
#         'X-No-Cache': 'true',
#     }
#     response = requests.get(url, headers=headers)
#     return response.json().get('data')

def jina_google_search(query):
    print('Looking for the answer to your question...')
    url = urlparse("https://s.jina.ai/" + query).geturl()
    headers = {
        'Accept': 'application/json',
        'X-No-Cache': 'true',
    }
    response = requests.get(url, headers=headers)
    print('Answers received.')
    return response.json()

def save_files(response):
    file_number = 0
    for webistes in response.get("data"):
        links = webistes.get("url")
        file_number += 1
        # check if rbi.org.in is in the url
        if 'rbi.org.in' in links:
            # get the content of the page
            website_scrape_data = webistes.get('content')
            # save the content to a file
            with open(f'azure/RBI_Guidelines_Documents/j_rbi_data_{file_number}.txt', 'w') as f:
                f.write('URL:'+links + '\n' + website_scrape_data)
                f.close()
            print(f"rbi_data_{file_number}.txt saved successfully.")

def main():
    # clear the directory "azure/RBI_Guidelines_Document" before saving new files
    for file in os.listdir('azure/RBI_Guidelines_Documents'):
        os.remove(f'azure/RBI_Guidelines_Documents/{file}')
    response = jina_google_search('What are the lastest RBI KYC guidelines for banks?')
    print('Answers received, now saving files...')
    save_files(response)