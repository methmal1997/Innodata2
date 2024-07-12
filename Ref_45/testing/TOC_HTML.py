import os.path

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded"
}

def fetch_html(url):
    response = requests.get(url,headers=headers, timeout=1000,allow_redirects=True)
    response.raise_for_status()
    return response.content

def html_content(toc_html,html_contents):
    combined_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Combined HTML</title>
    </head>
    <body>
    """

    for content in html_contents:
        soup = BeautifulSoup(content, 'html.parser')
        body = soup.find('body')
        combined_html += str(body) + "<br>"

    combined_html += """
    </body>
    </html>
    """

    with open(toc_html, 'w', encoding='utf-8') as file:
        file.write(combined_html)

def get_toc_html(current_out,TOC_name,languageList):
    html_contents = [fetch_html(url) for url in languageList]
    out_html=os.path.join(current_out,TOC_name)
    html_content(out_html, html_contents)
