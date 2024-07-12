import os
import re

import requests
import shutil
from bs4 import BeautifulSoup
from datetime import datetime
import common_function
import pandas as pd
import TOC_HTML

def get_soup(url):
    response = requests.get(url,headers=headers)
    soup= BeautifulSoup(response.content, 'html.parser')
    return soup

def print_bordered_message(message):
    border_length = len(message) + 4
    border = "-" * (border_length - 2)

    print(f"+{border}+")
    print(f"| {message} |")
    print(f"+{border}+")
    print()

def emailCompleted(Email_Sent,out_excel_file,url_id,duplicate_list,error_list,completed_list,ini_path,attachment,current_date,current_time,Ref_value,current_out):
    try:
        if str(Email_Sent).lower() == "true":
            attachment_path = out_excel_file
            if os.path.isfile(attachment_path):
                attachment = attachment_path
            else:
                attachment = None
            common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,
                                                 len(completed_list), ini_path, attachment, current_date,
                                                 current_time, Ref_value)
    except Exception as error:
        message = f"Failed to send email : {str(error)}"
        common_function.email_body_html(current_date, current_time, duplicate_list, error_list,
                                        completed_list,
                                        len(completed_list), url_id, Ref_value, attachment, current_out)
        #error_list.append(message)

    sts_file_path = os.path.join(current_out, 'Completed.sts')
    with open(sts_file_path, 'w') as sts_file:
        pass
    print_bordered_message("Scraping has been successfully completed for ID:" + url_id)

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
Total_count=None
ini_path=None
oneError=0

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
while url_index < len(url_list):
    try:
        url,url_id=url_list[url_index].split(',')
        current_datetime = datetime.now()
        current_date = str(current_datetime.date())
        current_time = current_datetime.strftime("%H:%M:%S")

        if url_check==0:
            print(url_id)
            ini_path = os.path.join(os.getcwd(), "Info.ini")
            Download_Path, Email_Sent, Check_duplicate, user_id = common_function.read_ini_file(ini_path)
            current_out = common_function.return_current_outfolder(Download_Path, user_id, url_id)
            out_excel_file = common_function.output_excel_name(current_out)
            TOC_name = common_function.output_TOC_name(current_out)

        Ref_value = "63"

        duplicate_list = []
        error_list = []
        completed_list=[]
        data = []

        pdf_count = 1

        current_soup=get_soup(url).find('div',class_='page page_issue_archive').find('ul').find('li')
        if current_soup.find('div',class_='series'):
            Year_Volume=current_soup.find('div',class_='series').text.strip().split(' ')
        else:
            Year_Volume=current_soup.find('a',class_='title').text.strip().split(' ')
        Issue=Year_Volume[3] if len(Year_Volume)==5 else ""
        Year = re.sub(r'[^0-9]+', '', Year_Volume[-1])
        Volume=Year_Volume[1]

        lastSoup=get_soup(current_soup.find('a',class_='title').get('href'))

        languageList=[i["href"] for i in lastSoup.find("div",class_="pkp_block block_language").find("ul").findAll("a")]
        pdf_paths=[]

        All_articles=lastSoup.find('div',class_='sections').findAll('div',class_='obj_article_summary')

        Total_count=len(All_articles)

        article_index, article_check = 0, 0
        while article_index < len(All_articles):
            Article_link,Article_title = None,None
            try:
                Article_link=All_articles[article_index].find('div',class_='title').find('a').get('href')
                Article_title = All_articles[article_index].find('div',class_='title').text.strip()
                Article_details=get_soup(Article_link)

                try:
                    Page_range_value=All_articles[article_index].find('div',class_='pages').text.strip()[0]
                    if Page_range_value == "e":
                        Identifier,Page_range=All_articles[article_index].find('div',class_='pages').text.strip(),""
                    else:
                        Identifier, Page_range = "",All_articles[article_index].find('div', class_='pages').text.strip()
                except:
                    Identifier, Page_range = "",""

                try:
                    DOI=Article_details.find('div',class_='item doi').find('span',class_='value').text.strip().rsplit('doi.org/',1)[-1]
                except:
                    DOI=""

                pdf_link=get_soup(Article_details.find('a',class_='obj_galley_link pdf').get('href')).find('a',class_='download').get('href')

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
                         "Identifier": Identifier,
                         "Volume": Volume, "Issue": Issue, "Supplement": "", "Part": "",
                         "Special Issue": "", "Page Range": Page_range, "Month": "", "Day": "",
                         "Year": Year,
                         "URL": pdf_link, "SOURCE File Name": f"{pdf_count}.pdf", "user_id": user_id,"TOC file Name":TOC_name})

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
                    message=f"Error link - {Article_link} : {str(error)}"
                    print("Download failed :",Article_title)
                    error_list.append(message)
                    article_index, article_check = article_index + 1, 0

        check = 0
        while check < 5:
            try:
                print("Wait until the TOC_HTML is downloaded")
                TOC_HTML.get_toc_html(current_out,TOC_name,languageList)
                check = 5
                print("TOC_HTML file downloaded successfully.")
            except:
                if not check < 4:
                    message = "Failed to get toc pdf"
                    error_list.append(message)
                check += 1

        try:
            common_function.sendCountAsPost(url_id, Ref_value, str(Total_count), str(len(completed_list)), str(len(duplicate_list)),
                            str(len(error_list)))
        except Exception as error:
            message=f"Failed to send post request : {str(error)}"
            error_list.append(message)

        if oneError<3:
            if len(error_list) == 0:
                emailCompleted(Email_Sent, out_excel_file, url_id, duplicate_list, error_list, completed_list, ini_path,
                               attachment, current_date, current_time, Ref_value, current_out)

            else:
                if oneError<2:
                    shutil.rmtree(current_out)
                    url_index=url_index-1
                    oneError += 1
                    print("Error links could be found from this site. The procedure will continue again for this ID.")

                else:
                    emailCompleted(Email_Sent, out_excel_file, url_id, duplicate_list, error_list, completed_list,
                                   ini_path,
                                   attachment, current_date, current_time, Ref_value, current_out)

        url_index, url_check = url_index + 1, 0
    except Exception as error:
        if url_check < 8:
            url_check += 1
        else:
            Error_message = "Error in the site:" + str(error)
            print(Error_message)
            error_list.append(Error_message)
            common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,
                                                 len(completed_list),
                                                 ini_path, attachment, current_date, current_time, Ref_value)
            # common_function.email_body_html(current_date, current_time, duplicate_list, error_list, completed_list,
            #                                 len(completed_list), url_id, Ref_value, attachment, current_out)

            url_index, url_check = url_index + 1, 0






