print("This is Ref_39")

import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# import undetected_chromedriver as uc
# import chromedriver_autoinstaller as chromedriver
# chromedriver.install()
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


headers2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded"
}

mainHeaders = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    #"Cookie": "didomi_token=eyJ1c2VyX2lkIjoiMTkwNzE5NTAtN2FjMC02ZWEwLWJmMTktYjZjOTM3NzA2MDc1IiwiY3JlYXRlZCI6IjIwMjQtMDctMDJUMDM6NTU6MTAuNjM2WiIsInVwZGF0ZWQiOiIyMDI0LTA3LTAyVDAzOjU1OjQyLjI1M1oiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiXX0sInZlbmRvcnNfbGkiOnsiZW5hYmxlZCI6WyJnb29nbGUiXX0sInZlcnNpb24iOjIsImFjIjoiQUZtQUNBRmsuQUZtQUNBRmsifQ==; euconsent-v2=CQBIJ4AQBIJ4AAHABBENA7EgALEAAELAAAqIF5wAQF5gXnABAXmAAAAA.diAACFgAAAAA; _gid=GA1.2.1451678636.1719892544; edimark_cart_hash=5tOk4cJrBDUgBupEoLzPNG6R2xGm5dbVPfgR0MWh9ETXymlAQ1IsoT1cZDZinvFLNsjxJYa6qeO8KhfnC3HFviqM8dyjpKaSw2SC; edimark_jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjo5MDk0LCJyZWZyZXNoIjoiNjY4MzdjZWJkMmExYSIsImlhdCI6MTcxOTg5MzIyNywiZXhwIjoxNzUxNDI5MjI3fQ.vx1y7AqCEPDoEHoNPNM0TR43AJz8umbXyyjlqCSPFoE; ci_session=872369f3ae11de0ded4db431055c6932c4ba8468; _gat_UA-9404591-1=1; _ga=GA1.1.157160225.1719892543; _ga_94MC5430DX=GS1.1.1719916393.2.1.1719917641.44.0.0",
    "Pragma": "no-cache",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

loginHeaders = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Content-Length": "96",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.edimark.fr",
    "Pragma": "no-cache",
    "Priority": "u=1, i",
    "Referer": "https://www.edimark.fr/",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

data = {
    "redirect": "https://www.edimark.fr/",
    "email": "bd-scm@elsevier.com",
    "password": "10739840",
    "persist": "1"
}

lastHeader = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Referer": "https://www.edimark.fr/",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

try:
    print("Process started...")
    print("This may take sometime.Please wait..........")

    try:
        with open('Source_title.txt', 'r', encoding='utf-8') as file:
            url_list = file.read().split('\n')
    except Exception as error:
        Error_message = "Error in the \"Source_title\" : " + str(error)
        print(Error_message)
        error_list.append(Error_message)
        common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,
                                             len(completed_list),
                                             ini_path, attachment, current_date, current_time, Ref_value)

    new_session = requests.session()
    url = "https://www.edimark.fr"
    post_url = 'https://www.edimark.fr/connexion'
    new_session.get(url, headers=mainHeaders)
    new_session.post(post_url, data=data, headers=loginHeaders)
    response = requests.get(url,headers=mainHeaders)

    current_soup = BeautifulSoup(response.content, 'html.parser')

    for i, url_url_id in enumerate(url_list):

        try:
            url_title, url_id = url_url_id.split(',')
            print(f"Executing this {url}")
            print(f"Executing this Source title {url_title}")
            current_datetime = datetime.now()
            current_date = str(current_datetime.date())
            current_time = current_datetime.strftime("%H:%M:%S")

            ini_path = os.path.join(os.getcwd(), "Info.ini")
            Download_Path, Email_Sent, Check_duplicate, user_id = common_function.read_ini_file(ini_path)

            data = []
            pdf_count = 1
            Ref_value = "39"
            current_out = common_function.return_current_outfolder(Download_Path, user_id, url_id)
            out_excel_file = common_function.output_excel_name(current_out)
            ul_object = current_soup.find("ul",class_="publications_sidebar_list")

            found_li = None
            for li_soup in ul_object:
                # print(li_soup.a.text.strip())
                if li_soup.a.text.strip() == url_title:
                    found_li = li_soup
                    break

            if not found_li:
                massage = f"Element not found for {url_title} id is {url_id}. So update Source_title.txt"
                error_list.append(massage)
                print(massage)

            li_id = li_soup.find('a')["data-magazine-id"]
            current_issue_link = f"https://www.edimark.fr/ajax/publications/{li_id}/"
            response2 = requests.get(current_issue_link, headers=mainHeaders)
            current_soup2 = BeautifulSoup(response2.content, 'html.parser')
            current = current_soup2.find("div",class_="p-3")
            issue_date = current.text.strip()

            issue_pattern = r"N° (\d+)"
            date_pattern = r"(\w+) (\d{4})"

            issue_match = re.search(issue_pattern, issue_date)
            if issue_match:
                issue = issue_match.group(1)
            else:
                issue = None

            date_match = re.search(date_pattern, issue_date)
            if date_match:
                month = date_match.group(1)
                year = date_match.group(2)
            else:
                month = None
                year = None
            print("Issue Number:", issue)
            print("Month:", month)
            print("Year:", year)

            Article_page_link = current.find("a")["href"]
            response3 = requests.get(Article_page_link, headers=mainHeaders)
            print(Article_page_link)

            current_soup3 = BeautifulSoup(response3.content, 'html.parser')
            Articles = current_soup3.find("div",class_="row-items").find_all("div",class_="row-item sidebar-visible")
            articles_count_with_pdf = len(Articles)
            print(f"articles_count_with_pdf {articles_count_with_pdf}")
            for article in Articles:
                Article_title = article.find("h3", class_="row-item-title").find("a").text
                Article_link = article.find("h3",class_="row-item-title").find("a")["href"]
                print(Article_title)
                soup = new_session.get(Article_link).content
                soup=BeautifulSoup(soup,"html.parser")

                Pdf_link = soup.find("button",id="reader_trigger")["source"]
                check_value, tpa_id = common_function.check_duplicate("", Article_title, url_id, "", issue)

                if Check_duplicate.lower() == "true" and check_value:
                    message = f"{Article_link} - duplicate record with TPAID : {tpa_id}"
                    duplicate_list.append(message)
                    print("Duplicate Article :", Article_link)
                else:
                    response_p = requests.get(Pdf_link, headers=headers2)
                    if response_p.status_code == 200:
                        pdf_content = response_p.content
                        output_fimeName = os.path.join(current_out, f"{pdf_count}.pdf")
                        with open(output_fimeName, 'wb') as file:
                            file.write(pdf_content)

                            data.append(
                                {"Title": Article_title, "DOI": "",
                                 "Publisher Item Type": "",
                                 "ItemID": "",
                                 "Identifier": "",
                                 "Volume": "", "Issue": issue, "Supplement": "",
                                 "Part": "",
                                 "Special Issue": "", "Page Range": "", "Month": month,
                                "Day": "",
                                 "Year": year,
                                 "URL": Pdf_link,
                                 "SOURCE File Name": f"{pdf_count}.pdf",
                                 "user_id": user_id})

                            df = pd.DataFrame(data)
                            df.to_excel(out_excel_file, index=False)
                            print(f"Downloaded the PDF file {pdf_count}")
                            pdf_count += 1
                            completed_list.append(Pdf_link)
                            with open('completed.txt', 'a', encoding='utf-8') as write_file:
                                write_file.write(Pdf_link + '\n')
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