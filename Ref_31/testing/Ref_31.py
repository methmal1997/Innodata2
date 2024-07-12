print("This is Ref_31")

import os
import re
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import common_function
import pandas as pd


def get_soup(url):
    response = requests.get(url,headers=headers,timeout=10000)
    soup= BeautifulSoup(response.content, 'html.parser')
    return soup


def get_month_year(Year_moth):
    if len(Year_moth)==3:
        Year,Month,Day=Year_moth[2],Year_moth[1],Year_moth[0]
    elif len(Year_moth)==2:
        Year, Month, Day = Year_moth[1], Year_moth[0], ""
    else:
        Year, Month, Day = Year_moth[0], "", ""
    return Year,Month,Day

def get_pdf_size(text):
    if "." in text:
        journal_name = re.search(r'PDF (.*?)\.', text).group(1)
    else:
        journal_name = re.search(r'PDF (.*?) kb', text).group(1)
    extracted_value = journal_name.replace(",", "") if "," in journal_name else journal_name
    extracted_value = int(extracted_value)
    return extracted_value

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
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

try:
    print("Process started...")
    print("This may take sometime.Please wait..........")

    try:
        with open('urlDetails.txt','r',encoding='utf-8') as file:
            url_list=file.read().split('\n')
    except Exception as error:
        Error_message = "Error in the \"urlDetails\" : " + str(error)
        print(Error_message)
        error_list.append(Error_message)
        common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,
                                             len(completed_list),
                                             ini_path, attachment, current_date, current_time, Ref_value)
        # common_function.email_body_html(current_date, current_time, duplicate_list, error_list, completed_list,
        #                                 len(completed_list), url_id, Ref_value, attachment, current_out)

    try:
        with open('completed.txt', 'r', encoding='utf-8') as read_file:
            read_content = read_file.read().split('\n')
    except FileNotFoundError:
        with open('completed.txt', 'w', encoding='utf-8'):
            with open('completed.txt', 'r', encoding='utf-8') as read_file:
                read_content = read_file.read().split('\n')

    url_index, url_check = 0, 0
    for i, url_url_id in enumerate(url_list):
        try:
            attachment = None
            url, url_id = url_list[url_index].split(',')
            print(f"Executing this {url}")
            current_datetime = datetime.now()
            current_date = str(current_datetime.date())
            current_time = current_datetime.strftime("%H:%M:%S")

            ini_path = os.path.join(os.getcwd(), "Info.ini")
            Download_Path, Email_Sent, Check_duplicate, user_id = common_function.read_ini_file(ini_path)

            data = []
            pdf_count = 1
            Ref_value = "31"
            url_value = url.split('/')[-2]
            current_out = common_function.return_current_outfolder(Download_Path, user_id, url_id)
            out_excel_file = common_function.output_excel_name(current_out)

            current_soup=get_soup('https://www.ingentaconnect.com'+get_soup(url).find('ul',class_='bobby').find('li',class_='rowShade').find('a').get('href'))
            find_volume=current_soup.find('div', class_='left-col')
            if find_volume.find('i'):
                remove_ele=find_volume.find('i')
                remove_ele.extract()
            Volume_issue_year = find_volume.text.strip().split(",")
            Volume=re.sub(r'[^0-9]+',"",Volume_issue_year[0])
            Issue=re.sub(r'[^0-9]+',"",Volume_issue_year[1])
            Year,Month,Day=get_month_year(Volume_issue_year[-1].split())
            print(f"{Year} {Volume} {Issue}")
            All_articles=current_soup.find('div',class_='greybg').findAll('div',class_='data')

            Total_count=len(All_articles)

            article_index, article_check = 0, 0
            while article_index < len(All_articles):
                Article_link,Article_title=None,None
                try:
                    Article_title=All_articles[article_index].find('div',class_='ie5searchwrap').a.text.strip()
                    Article_link="https://www.ingentaconnect.com"+All_articles[article_index].find('div',class_='ie5searchwrap').a.get('href')
                    Article_details=get_soup(Article_link)
                    Page_range=re.search(r'p. (.*?)\(', All_articles[article_index].find('div',class_='ie5searchwrap').find('p').text.strip()).group(1)
                    DOI=Article_details.findAll('div',class_='supMetaData')[-1].findAll('p')[-1].text.strip().rsplit("org/",1)[-1] if (
                            len(Article_details.findAll('div',class_='supMetaData')[-1].findAll('p'))==3) else ""
                    pdf_link=Article_link[:-1]+"?crawler=true&mimetype=application/pdf" if Article_link[-1]=="#" else Article_link+"?crawler=true&mimetype=application/pdf"

                    check_value, tpa_id = common_function.check_duplicate(DOI, Article_title, url_id, Volume, Issue)
                    if Check_duplicate.lower() == "true" and check_value:
                        message = f"{Article_link} - duplicate record with TPAID : {tpa_id}"
                        duplicate_list.append(message)
                        print("Duplicate Article :", Article_title)

                    else:
                        pdf_content = requests.get(pdf_link, headers=headers).content
                        output_fimeName = os.path.join(current_out, f"{pdf_count}.pdf")
                        with open(output_fimeName, 'wb') as file:
                            file.write(pdf_content)
                        data.append(
                            {"Title": Article_title, "DOI": DOI, "Publisher Item Type": "", "ItemID": "",
                             "Identifier": "",
                             "Volume": Volume, "Issue": Issue, "Supplement": "", "Part": "",
                             "Special Issue": "", "Page Range": Page_range, "Month": Month, "Day": Day,
                             "Year": Year,
                             "URL": Article_link, "SOURCE File Name": f"{pdf_count}.pdf", "user_id": user_id})
                        df = pd.DataFrame(data)
                        df.to_excel(out_excel_file, index=False)
                        pdf_count += 1
                        scrape_message = f"{Article_link}"
                        completed_list.append(scrape_message)
                        print("Original Article :", Article_title)

                    if not Article_link in read_content:
                        with open('completed.txt', 'a', encoding='utf-8') as write_file:
                            write_file.write(Article_link + '\n')

                    article_index, article_check = article_index + 1, 0

                except Exception as error:
                    if article_check < 4:
                        article_check += 1
                    else:
                        message = f"{Article_link} : {str(error)}"
                        print("Download failed :", Article_title)
                        error_list.append(message)
                        article_index, article_check = article_index + 1, 0

            try:
                common_function.sendCountAsPost(url_id, Ref_value, str(Total_count), str(len(completed_list)), str(len(duplicate_list)),
                                str(len(error_list)))
            except Exception as error:
                message=f"Failed to send post request : {str(error)}"
                error_list.append(message)

            try:
                if str(Email_Sent).lower()=="true":
                    attachment_path = out_excel_file
                    if os.path.isfile(attachment_path):
                        attachment = attachment_path
                    else:
                        attachment = None
                    common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,
                                                         len(completed_list), ini_path, attachment, current_date,
                                                         current_time, Ref_value)
                    # common_function.email_body_html(current_date, current_time, duplicate_list, error_list, completed_list,
                    #                                 len(completed_list), url_id, Ref_value, attachment, current_out)
            except Exception as error:
                message=f"Failed to send email : {str(error)}"
                common_function.email_body_html(current_date, current_time, duplicate_list, error_list, completed_list,
                                                len(completed_list), url_id, Ref_value, attachment, current_out)
                error_list.append(message)

            sts_file_path = os.path.join(current_out, 'Completed.sts')
            with open(sts_file_path, 'w') as sts_file:
                pass
            url_index, url_check = url_index + 1, 0
        except Exception as error:
            if url_check < 4:
                url_check += 1
            else:
                try:
                    Error_message = "Error in the site:" + str(error)
                    print(Error_message,"\n")
                    error_list.append(Error_message)
                    url_index, url_check = url_index + 1, 0
                    common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,
                                                         len(completed_list),
                                                         ini_path, attachment, current_date, current_time, Ref_value)


                except Exception as error:
                    message = f"Failed to send email : {str(error)}"
                    print(message)
                    common_function.email_body_html(current_date, current_time, duplicate_list, error_list, completed_list,
                                                    len(completed_list), url_id, Ref_value, attachment, current_out)
                    error_list.append(message)

except:
    Error_message = "Error in the main process :"

    error_list.append(str(Error_message))
    log_file_path = os.path.join('log.txt')
    with open(log_file_path, 'w') as log_file:
        log_file.write(str(Error_message) + '\n')