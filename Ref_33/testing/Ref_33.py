print("This is Ref_33")

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
attachment=None
url_id=None
current_date=None
current_time=None
Ref_value=None
ini_path=None

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

    for i, url_url_id in enumerate(url_list):

        try:
            url, url_id = url_url_id.split(',')
            print(f"Executing this {url}")
            current_datetime = datetime.now()
            current_date = str(current_datetime.date())
            current_time = current_datetime.strftime("%H:%M:%S")

            ini_path = os.path.join(os.getcwd(), "Info.ini")
            Download_Path, Email_Sent, Check_duplicate, user_id = common_function.read_ini_file(ini_path)

            data = []
            pdf_count = 1
            Ref_value = "33"
            url_value = url.split('/')[-2]
            current_out = common_function.return_current_outfolder(Download_Path, user_id, url_id)
            out_excel_file = common_function.output_excel_name(current_out)
            url_orginal = url
            url = url + "issue/archive"

            response = requests.get(url, headers=headers, timeout=1000, allow_redirects=True)
            current_soup = BeautifulSoup(response.content, 'html.parser')
            current_issue = current_soup.find('div', class_="issue span9 issue_month")
            current_issue_link = current_issue.find("a")["href"]

            print(current_issue_link)

            v_date_year = current_issue.text.strip()
            pattern = r'Vol (\d+) \((\w+ \d+, \d+)\):'

            match = re.search(pattern, v_date_year)

            if match:
                volume = match.group(1)
                full_date = match.group(2)
                month, date, year = full_date.split()
            print(f"{month} {year} {date} {volume} ")

            response = requests.get(current_issue_link, headers=headers, timeout=1000,allow_redirects=True)
            current_soup = BeautifulSoup(response.content, 'html.parser')
            Articles = current_soup.findAll('div',class_="section")
            articles_count_with_pdf = len(Articles)
            print(f"articles_count_with_pdf {articles_count_with_pdf}")
            pdf_list = []
            for article in Articles:
                Article_link = url_orginal + article.find("a")["href"][1:]

                print(Article_link)
                response2 = requests.get(Article_link, headers=headers, timeout=1000, allow_redirects=True)
                current_soup2 = BeautifulSoup(response2.content, 'html.parser')

                Article_title = current_soup2.find("h1",class_="title").text
                print(Article_title)
                DOI_text = current_soup2.find("div",class_="doi-number color-bg").text

                doi_pattern = r"doi:\s*(10\.\d{4,9}/[-._;()/:A-Z0-9]+)"
                doi_match = re.search(doi_pattern, DOI_text, re.IGNORECASE)
                DOI_text = doi_match.group(1) if doi_match else None

                DOI = DOI_text.replace("Cite", "")

                date_element = current_soup2.find("a",class_="hierarchyLink").text.strip()

                volume_match = re.search(r'Vol (\d+)', date_element)
                volume = volume_match.group(1) if volume_match else None

                date_pattern_with_day = r'\((\w+) (\d+), (\d+)\)'
                date_pattern_without_day = r'\((\w+) (\d+)\)'

                date_match = re.search(date_pattern_with_day, date_element)
                if date_match:

                    month = date_match.group(1)
                    day = date_match.group(2)
                    year = date_match.group(3)
                else:

                    date_match = re.search(date_pattern_without_day, date_element)

                    if date_match:
                        month = date_match.group(1)
                        day = None  # No day in this pattern
                        year = date_match.group(2)
                    else:
                        # No match found
                        month = None
                        day = None
                        year = None

                print(month)
                print(year)
                print(day)
                print(volume)

                Pdf_link = current_soup2.find("a",class_="pdf")["href"]
                response3 = requests.get(Pdf_link, headers=headers, timeout=100, allow_redirects=True)
                current_soup3 = BeautifulSoup(response3.content, 'html.parser')

                Pdf_link = current_soup3.find("a",id="pdfDownloadLink")["href"]

                check_value, tpa_id = common_function.check_duplicate(DOI, Article_title, url_id, volume, "")

                if Check_duplicate.lower() == "true" and check_value:
                    message = f"{Article_link} - duplicate record with TPAID : {tpa_id}"
                    duplicate_list.append(message)
                    print("Duplicate Article :", Article_link)
                else:
                    if Article_title not in pdf_list:
                        print(Pdf_link)
                        response_2 = requests.get(Pdf_link, headers=headers2,timeout=1000,allow_redirects=True)
                        if response_2.status_code == 200:
                            pdf_content = response_2.content
                            output_fimeName = os.path.join(current_out, f"{pdf_count}.pdf")
                            with open(output_fimeName, 'wb') as file:
                                file.write(pdf_content)

                                data.append(
                                    {"Title": Article_title, "DOI": DOI,
                                     "Publisher Item Type": "",
                                     "ItemID": "",
                                     "Identifier": "",
                                     "Volume": volume, "Issue": "", "Supplement": "",
                                     "Part": "",
                                     "Special Issue": "", "Page Range": "", "Month": month,
                                    "Day": day,
                                     "Year": year,
                                     "URL": Pdf_link,
                                     "SOURCE File Name": f"{pdf_count}.pdf",
                                     "user_id": user_id})

                                df = pd.DataFrame(data)
                                df.to_excel(out_excel_file, index=False)
                                print(f"Downloaded the PDF file {pdf_count}")
                                pdf_count += 1
                                completed_list.append(Article_link)
                                with open('completed.txt', 'a', encoding='utf-8') as write_file:
                                    write_file.write(Pdf_link + '\n')
                                pdf_list.append(Article_title)
                                print("###################################")

            try:
                common_function.sendCountAsPost(url_id, Ref_value, str(articles_count_with_pdf),
                                                str(len(completed_list)),
                                                str(len(duplicate_list)),
                                                str(len(error_list)))
            except Exception as error:
                message = str(error)
                print("New update")
                error_list.append(message)

            if str(Email_Sent).lower() == "true":
                attachment_path = out_excel_file
                if os.path.isfile(attachment_path):
                    attachment = attachment_path
                else:
                    attachment = None
                common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,
                                                     len(completed_list), ini_path, attachment, current_date,
                                                     current_time, Ref_value)

            sts_file_path = os.path.join(current_out, 'Completed.sts')
            with open(sts_file_path, 'w') as sts_file:
                pass

        except Exception as error:
            Error_message = f"Error in the site: {error}"
            print(Error_message, "\n")
            error_list.append(Error_message)
            common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,
                                                 len(completed_list),
                                                 ini_path, attachment, current_date, current_time, Ref_value)

except:
    Error_message = "Error in the main process :"

    error_list.append(str(Error_message))
    log_file_path = os.path.join('log.txt')
    with open(log_file_path, 'w') as log_file:
        log_file.write(str(Error_message) + '\n')