print("This is Ref_51")

import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import undetected_chromedriver as uc
import chromedriver_autoinstaller as chromedriver
chromedriver.install()
from bs4 import BeautifulSoup
import re
import certifi
import os
import sys
from datetime import datetime
import common_function
import pandas as pd
import requests
import warnings

warnings.filterwarnings("ignore")

import logging

urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

duplicate_list = []
error_list = []
completed_list = []
attachment = None
url_id = None
current_date = None
current_time = None
Ref_value = None
ini_path = None

options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--incognito')
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-popup-blocking')
options.add_argument('--user-agent=YOUR_USER_AGENT_STRING')
options.add_argument('--version_main=108')
driver = uc.Chrome(options=options)

headers2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded"
}

try:
    print("Process started...")
    print("This may take sometime.Please wait..........")

    try:
        with open('urlDetails.txt', 'r', encoding='utf-8') as file:
            url_list = file.read().split('\n')
    except Exception as error:
        Error_message = "Error in the \"urlDetails\" : " + str(error)
        print(Error_message)
        error_list.append(Error_message)
        common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,
                                             len(completed_list),
                                             ini_path, attachment, current_date, current_time, Ref_value)
except:
    pass

for i, url_url_id in enumerate(url_list):

    url, url_id = url_url_id.split(',')
    url = "https://www.scielo.br/j/po/grid"
    print(f"Executing this {url}")
    current_datetime = datetime.now()
    current_date = str(current_datetime.date())
    current_time = current_datetime.strftime("%H:%M:%S")

    ini_path = os.path.join(os.getcwd(), "Info.ini")
    Download_Path, Email_Sent, Check_duplicate, user_id = common_function.read_ini_file(ini_path)

    data = []
    pdf_count = 1
    Ref_value = "51"
    url_value = url.split('/')[-2]
    current_out = common_function.return_current_outfolder(Download_Path, user_id, url_id)
    out_excel_file = common_function.output_excel_name(current_out)

    response = requests.get(url, headers=headers, timeout=50, allow_redirects=True)
    current_soup = BeautifulSoup(response.content, 'html.parser')
    pdf_list = []

    table = current_soup.findAll('table')[0]
    latest_issue_url = "https://www.scielo.br" + table.findAll("td", class_="left")[1].findAll("a")[-1][
        "href"]

    response2 = requests.get(latest_issue_url, headers=headers, timeout=1000, allow_redirects=True)
    current_soup2 = BeautifulSoup(response2.content, 'html.parser')

    vol_issue = current_soup2.find("div",class_='collapse-content issueIndent').text.strip()
    print(vol_issue)

    pattern = r"Volume: (\d+), Número: (\d+), Publicado: (\d{4})(?:-(\d{2})-(\d{2}))?"
    pattern2 = r"Volume: (\d+), Issue: (\d+), Published: (\d{4})(?:-(\d{2})-(\d{2}))?"
    pattern3 = r"Volume: (\d+), Issue: (\d+), Publicado: (\d{4})(?:-(\d{2})-(\d{2}))?"
    match = re.search(pattern, vol_issue)
    match2 = re.search(pattern2, vol_issue)
    match3 = re.search(pattern3, vol_issue)
    volume,issue,year,month,day = None,None,None,None,None
    # Search for the pattern in the input string
    match = re.search(pattern, vol_issue)
    match2 = re.search(pattern2, vol_issue)
    match3 = re.search(pattern3, vol_issue)
    if match:
        volume = match.group(1)
        issue = match.group(2)
        year = match.group(3)
        month = match.group(4)
        day = match.group(5)
    elif match2:
        volume = match2.group(1)
        issue = match2.group(2)
        year = match2.group(3)
        month = match2.group(4)
        day = match2.group(5)
    else:
        volume = match3.group(1)
        issue = match3.group(2)
        year = match3.group(3)
        month = match3.group(4)
        day = match3.group(5)
    print(volume)
    print(issue)
    print(year)
    print(month)
    print(day)
    # print(latest_issue_url)

    # Articles = current_soup2.findAll("div",class_="issueIndent")[1].find("ul",class_="articles").findAll("li")
    issue_indent_div = current_soup2.findAll("div", class_="issueIndent")[1]
    articles_ul = issue_indent_div.find("ul", class_="articles")
    first_li = articles_ul.find("li")
    Articles = []
    Articles.append(first_li)
    next_li = first_li.find_next_sibling("li")
    while next_li:
        Articles.append(next_li)
        next_li = next_li.find_next_sibling("li")
    print(len(Articles))
    for sibling in Articles:
        print(sibling.find("h2").text.strip())
        print(sibling.find("a",title="English"))
        print(sibling)
        print("#########################3")
