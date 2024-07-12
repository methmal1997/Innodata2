print("This is Ref_51")

import json
import urllib3
from calendar import month_name, month_abbr
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


def convert_month_names(input_string):
    month_dict = {
        "Jan": "January",
        "Feb": "February",
        "Mar": "March",
        "Apr": "April",
        "May": "May",
        "Jun": "June",
        "Jul": "July",
        "Aug": "August",
        "Sept": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December"
    }
    pattern = r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\b'

    def replace_month(match):
        return month_dict[match.group(1)]
    result = re.sub(pattern, replace_month, input_string)
    return result


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
            Ref_value = "51"
            url_value = url.split('/')[-2]
            current_out = common_function.return_current_outfolder(Download_Path, user_id, url_id)
            out_excel_file = common_function.output_excel_name(current_out)

            new_session = requests.session()
            new_session.get("https://www.scielo.br/set_locale/en/",timeout=1000, allow_redirects=True)

            pdf_list = []
            try:
                response = new_session.get(url, headers=headers, timeout=1000, allow_redirects=True)
                current_soup = BeautifulSoup(response.content, 'html.parser')
                table = current_soup.findAll('table')[0]
                latest_issue_url = "https://www.scielo.br" + table.findAll("td", class_="left")[1].findAll("a")[-1][
                    "href"]
                response2 = new_session.get(latest_issue_url, headers=headers, timeout=1000, allow_redirects=True)
                current_soup2 = BeautifulSoup(response2.content, 'html.parser')
                vol_issue = current_soup2.find("div",class_='collapse-content issueIndent').text.strip()
                pattern = r"Volume: (\d+), Número: (\d+), Publicado: (\d{4})(?:-(\d{2})-(\d{2}))?"
                pattern2 = r"Volume: (\d+), Issue: (\d+), Published: (\d{4})(?:-(\d{2})-(\d{2}))?"
                pattern3 = r"Volume: (\d+), Issue: (\d+), Publicado: (\d{4})(?:-(\d{2})-(\d{2}))?"
                pattern4 = r'Volume: (\d+), Published: (\d{4})'
                match = re.search(pattern, vol_issue)
                match2 = re.search(pattern2, vol_issue)
                match3 = re.search(pattern3, vol_issue)
                match4 = re.search(pattern4, vol_issue)

                volume,issue,year,month,day = None,None,None,None,None
                print(vol_issue)
                match = re.search(pattern, vol_issue)
                match2 = re.search(pattern2, vol_issue)
                match3 = re.search(pattern3, vol_issue)
                try:
                    if match:
                        volume = match.group(1)
                        issue = match.group(2)
                        year = match.group(3)
                        month = match.group(4)
                        # day = match.group(5)
                    elif match2:
                        volume = match2.group(1)
                        issue = match2.group(2)
                        year = match2.group(3)
                        month = match2.group(4)
                        # day = match2.group(5)
                    elif match3:
                        volume = match3.group(1)
                        issue = match3.group(2)
                        year = match3.group(3)
                        month = match3.group(4)
                        # day = match3.group(5)
                    elif match4:
                        volume = match4.group(1)
                        year = match4.group(2)
                except:
                    pass
                print(volume)
                print(issue)
                print(year)
                print(month)
                print(day)
                # print(latest_issue_url)

                issue_indent_div = current_soup2.findAll("div", class_="issueIndent")[1]
                articles_ul = issue_indent_div.find("ul", class_="articles")
                first_li = articles_ul.find("li")
                Articles = []
                Articles.append(first_li)
                next_li = first_li.find_next_sibling("li")
                while next_li:
                    Articles.append(next_li)
                    next_li = next_li.find_next_sibling("li")

                articles_count_with_pdf = len(Articles)
                print(f"No of articles {articles_count_with_pdf}")
                for article in Articles:
                    try:
                        try:
                            Article_title = ''.join(element.strip() for element in article.find("h2").contents if not getattr(element, 'name', None) == 'span').strip()
                        except:
                            Article_title = article.find("h2").text.strip()

                        try:
                            Article_link = "https://www.scielo.br" + article.find("a",title="Espanhol")["href"]
                        except:
                            try:
                                Article_link = "https://www.scielo.br" + article.find("a", title="Spanish")["href"]
                            except:
                                try:
                                    Article_link = "https://www.scielo.br" + article.find("a", title="English")["href"]
                                except:
                                    Article_link = "https://www.scielo.br" + article.find("a", title="Inglês")["href"]
                        response3 = new_session.get(Article_link, headers=headers, timeout=1000,
                                                 allow_redirects=True)
                        current_soup3 = BeautifulSoup(response3.content, 'html.parser')
                        DOI_text = current_soup3.find("a",class_="_doi")['href']
                        pattern = r"https://doi.org/(10\.\d{4,9}/[-._;()/:A-Z0-9]+)"

                        match = re.search(pattern, DOI_text, re.IGNORECASE)
                        if match:
                            DOI = match.group(1)

                        print(DOI)
                        print(Article_title)
                        # print(Article_link)
                        Pdf_link =  '/'.join(url.split('/')[:3]) + current_soup3.find("ul", class_="dropdown-menu menu-share-mobile").findAll("li")[-1].find("a")["href"]
                        print(Pdf_link)
                        print("#########")

                        check_value, tpa_id = common_function.check_duplicate(DOI, Article_title, url_id, volume,
                                                                              issue)
                        if Check_duplicate.lower() == "true" and check_value:
                            message = f"{Article_link} - duplicate record with TPAID : {tpa_id}"
                            duplicate_list.append(message)
                            print("Duplicate Article :", Article_link)
                        else:
                            if Article_title not in pdf_list:
                                response_2 = new_session.get(Pdf_link, headers=headers2)
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
                                             "Volume": volume, "Issue": issue, "Supplement": "",
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
                                        completed_list.append(Pdf_link)
                                        with open('completed.txt', 'a', encoding='utf-8') as write_file:
                                            write_file.write(Pdf_link + '\n')
                                        pdf_list.append(Article_title)
                                        print("###################################")
                    except:
                        try:
                            Article_link = "https://www.scielo.br" + article.find("a", title="Espanhol")["href"]
                            print(f" Failed to download article {Article_link}")
                        except:
                            pass

            except:
                response = requests.get(url, headers=headers, timeout=1000, allow_redirects=True)
                current_soup = BeautifulSoup(response.content, 'html.parser')
                table = current_soup.findAll('table')[3]
                rows = table.find_all('tr')

                hrefs = []
                max_tag_not_found = True
                while max_tag_not_found:
                    for i in range(0,len(rows)):
                        for row in rows[i]:
                            for cell in row:
                                link = cell.find('a')
                                if link:
                                    hrefs.append(link)
                        max_number = -1
                        max_anchor_tag = None
                        for anchor_tag in hrefs:
                            try:
                                try:
                                    number = int(anchor_tag.text.strip())
                                except ValueError:
                                    continue
                                if number > max_number:
                                    max_number = number
                                    max_anchor_tag = anchor_tag
                            except:
                                pass
                        if max_anchor_tag:
                            max_tag_not_found = False
                            break
                            pass
                        else:
                            print("strugguling find latest issue")
                latest_issue_url = max_anchor_tag["href"].replace("http://", "https://")
                print(latest_issue_url)
                response2 = new_session.get(latest_issue_url, headers=headers, timeout=1000, allow_redirects=True)
                current_soup2 = BeautifulSoup(response2.content, 'html.parser')

                p_left = current_soup2.find("p",align="left").text.strip()
                match = re.search(r'no\.(\d+)\s+Valdivia\s+(\d{4})', p_left)
                match2 = re.search(r'no\.(\d+)\s+Valparaíso\s+(\d{4})', p_left)
                month = None
                day = None
                issue = None
                volume = None
                year = None
                if match:
                    volume = match.group(1)
                    year = match.group(2)
                elif match2:
                    volume = match2.group(1)
                    year = match2.group(2)
                else:
                    pattern = r'vol\.(\d+)\s.*?\b(\w+)\b\.\s(\d{4})'
                    matches = re.search(pattern, p_left)

                    if matches:
                        volume = matches.group(1)
                        month = matches.group(2)
                        month = convert_month_names(month)
                        year = matches.group(3)

                print(volume)
                print(year)
                print(month)
                print(day)
                print(issue)
                table = current_soup2.findAll('table')[3]
                hrefs = []
                for row in table:
                    for cell in row:
                        link = cell.find("a",text='texto en  Español')
                        if link:
                            hrefs.append(link["href"])
                        else:
                            link = cell.find("a", text='text in  Spanish')
                            if link:
                                hrefs.append(link["href"])

                articles_count_with_pdf = len(hrefs)

                if articles_count_with_pdf == 0:
                    table = current_soup2.findAll('table')[4]
                    hrefs = []
                    for row in table:
                        for cell in row:
                            link = cell.find("a", text='text in  Spanish')
                            if link:
                                hrefs.append(link["href"])
                            else:
                                link = cell.find("a", text='texto en  Español')
                                if link:
                                    hrefs.append(link["href"])

                    articles_count_with_pdf = len(hrefs)

                k = []
                print(f"No of articles {articles_count_with_pdf}")
                for Article_link in hrefs:
                    response3 = requests.get(Article_link, headers=headers, timeout=1000, allow_redirects=True)
                    current_soup3 = BeautifulSoup(response3.content, 'html.parser')
                    print("#################################")
                    try:
                        try:
                            try:
                                Article_title = current_soup3.find("p",class_="trans-title").text
                            except:
                                Article_title = current_soup3.find("p",class_='title').text
                        except:
                            Article_title = current_soup3.find("meta",name="citation_title")["content"]
                        DOI_text = current_soup3.find("h4", id="doi").text.strip()
                        pattern = r"10\.\d{4,9}/[-._;()/:A-Z0-9]+"
                        match = re.search(pattern, DOI_text, re.IGNORECASE)
                        if match:
                            DOI = match.group(0)

                        Pdf_link = '/'.join(url.split('/')[:3]) + current_soup3.findAll("div",class_="box")[1].findAll("li")[1].find('a')["href"]
                        print(Article_title)
                        print(DOI)
                        print(Pdf_link)

                        try:
                            requests.get(Pdf_link, headers=headers2)
                        except:
                            Pdf_link =  "https://ve.scielo.org" + current_soup3.findAll("div", class_="box")[1].findAll("li")[0].find('a')["href"]
                            print(Pdf_link)


                        "https://ve.scielo.org/pdf/og/v82n3/0048-7732-og-82-03-284.pdf"
                        "https://ve.scielo.org/pdf/og/v82n3/0048-7732-og-82-03-284.pdf"

                        check_value, tpa_id = common_function.check_duplicate(DOI, Article_title, url_id, volume, "")

                        if Check_duplicate.lower() == "true" and check_value:
                            message = f"{Article_link} - duplicate record with TPAID : {tpa_id}"
                            duplicate_list.append(message)
                            print("Duplicate Article :", Article_link)
                        else:
                            if Article_title not in pdf_list:
                                response_2 = requests.get(Pdf_link, headers=headers2)
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
                                        completed_list.append(Pdf_link)
                                        with open('completed.txt', 'a', encoding='utf-8') as write_file:
                                            write_file.write(Pdf_link + '\n')
                                        pdf_list.append(Article_title)
                                        print("###################################")

                    except:
                        print(f" Failed to download article {Article_link}")
                        pass

                print("##########################")



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

# strcutre is diiferent
"https://www.scielo.br/j/gp/grid"
"https://www.scielo.br/j/jvatitd/grid"
"https://www.scielo.br/j/agora/grid"
"https://www.scielo.br/j/rpp/grid"

# Not work
"http://www.scielo.org.co/scielo.php?script=sci_issues&pid=2248-6046&lng=en&nrm=iso"

# no artciles
"http://www.scielo.org.ve/scielo.php?script=sci_issues&pid=0048-7732&lng=en"
"https://www.scielo.cl/scielo.php?script=sci_issues&pid=0717-7526&lng=en&nrm=iso"

