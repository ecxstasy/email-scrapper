from collections import deque
import re
from bs4 import BeautifulSoup
#pip install BeautifulSoup
import requests
import urllib.parse

user_url = str(input("[+] enter url: "))
urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0

try:
    while True:
        count += 1
        if count > 10:
            break
            
        url = urls.popleft()
        scraped_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = f'{parts.scheme}://{parts.netloc}'
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
        
        print(f'{count} processing {url}')
        
        try:
            response = requests.get(url)
        except(requests.exception.MissingSchema, requests.exception.ConnectionError):
            continue
            
        new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.-]+\.[a-z]+', response.text, re.I))
        emails.update(new_emails)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        for anchor in soup.find_all('a'):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)
                
except KeyboardInterrupt:
    print('[-] closing')

print('\nDone.')
print(f'{len(emails)} found()\n')

for mail in emails:
    print(' ' + mail)

print('\n')
