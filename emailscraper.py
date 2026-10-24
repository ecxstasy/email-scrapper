from collections import deque
import re
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import requests
import urllib.parse

user_url = input("[+] enter url: ").strip()
urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0
limit = int(input('[+] enter search limits: '))

try:
    while urls and count < limit:
        url = urls.popleft()
        if url in scraped_urls:
            continue
        scraped_urls.add(url)

        count += 1
        print(f'{count} processing {url}')

        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException:
            continue

        new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.-]+\.[a-z]+', response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, 'html.parser')
        for anchor in soup.find_all('a', href=True):
            link = anchor['href'].strip()

            if link.startswith(('mailto:', 'javascript:', 'tel:', '#')) or not link:
                continue

            link = urllib.parse.urljoin(url, link)
            link = urllib.parse.urldefrag(link)[0]

            if link.startswith('http') and link not in urls and link not in scraped_urls:
                urls.append(link)

except KeyboardInterrupt:
    print('[-] closing')

print('\nDone.')
print(f'{len(emails)} found\n')

for mail in emails:
    print(' ' + mail)

print('\n')
