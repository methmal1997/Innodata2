import requests
from bs4 import BeautifulSoup
import os
import re
import common_function
from datetime import datetime
import pandas as pd
import time
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller as chromedriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tempfile

chromedriver.install()


def get_soup_using_requests(url, headers, cookies_dict):
    cookies = {key: value for key, value in cookies_dict.items()}
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)
    response = session.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup
def init_public_driver(download_path):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--user-agent=YOUR_USER_AGENT_STRING')

    prefs = {'download.default_directory': download_path}
    options.add_experimental_option('prefs', prefs)

    driver = None
    errors = []

    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        errors.append(str(e))

    return driver, errors

def get_driver_content(url, driver):
    driver.get(url)
    content = driver.page_source
    cookies = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in driver.get_cookies()])
    soup = BeautifulSoup(content, 'html.parser')
    return soup, cookies

def download_pdf(url, current_out):
    try:
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(url)
        response.raise_for_status()
        output_fimeName = os.path.join(current_out, f"{pdf_count}.pdf")
        with open(output_fimeName, 'wb') as f:
            f.write(response.content)
            print(f"Downloaded: {output_fimeName}")
    except Exception as e:
        print(f"PDF download failed from {url}: {e}")

def get_driver_pdf(url, new_filename, download_path, driver, error_list):
    # Delete any existing PDF files in the download path
    for file in os.listdir(download_path):
        if file.endswith(".pdf"):
            os.remove(os.path.join(download_path, file))
    try:
        driver.get(url)
        time.sleep(5)

        while any(f.endswith('.crdownload') for f in os.listdir(download_path)):
            time.sleep(1)
        # Check if a PDF file was downloaded
        pdf_files = [f for f in os.listdir(download_path) if f.endswith(".pdf")]
        if pdf_files:
            downloaded_file = os.path.join(download_path, pdf_files[0])
            shutil.move(downloaded_file, new_filename)
            print(f"Downloaded: {new_filename}")
        else:
            error_list.append(f"PDF download failed. url: "+url)
    except Exception as e:
        error_list.append(f"PDF download failed. url: "+url)

def return_api_key():
    try:
        with open('API_KEY.txt','r') as file:
            content=file.read().strip()
            return content
    except Exception as e:
        error_list.append(e)
        print(e)

def get_selenium_cookies(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)
    selenium_cookies = driver.get_cookies()
    driver.quit()
    cookies_dict = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
    return cookies_dict

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
cookies = {
    "_hjSession_360107": "eyJpZCI6IjU2ZTI2ODg1LWZiYmEtNGRmNy05MGMxLTc5NzlhZTFlMjZjYiIsImMiOjE3MTg3NjI1MTk5NzAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=",
    "_hjSessionUser_360107": "eyJpZCI6IjExZWNkNTIwLWNlZGUtNWIxMC05OGM3LTI4OGFlZDc2MTgxNyIsImNyZWF0ZWQiOjE3MTg3NjI1MTk5NjksImV4aXN0aW5nIjpmYWxzZX0=",
    "_ga_1G284LDK06": "GS1.1.1718762518.1.0.1718762518.0.0.0",
    "__utmt": "1",
    "__utma": "136797536.1526303384.1718762517.1718762517.1718762517.1",
    "__cf_bm": "InH6IwgbnBysGzHe76M2s7GAQAmmO_yNT9DJhkJd1PQ-1718762516-1.0.1.1-n5yUpVPP5e5DHhVJuRZvbWIMA3csNXGlRqc3GgyD7GsVFKy0bEFwuVJyDDqpsHxvuKLztzmdcEhohXntFwO._Q",
    "__utmb": "136797536.1.10.1718762517",
    "timezone": "330",
    "__utmz": "136797536.1718762517.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "JSESSIONID": "04DF41D5A2FC6ECB776D9C8BB626F98D",
    "MACHINE_LAST_SEEN": "2024-06-18T19%3A01%3A56.196-07%3A00",
    "MAID": "UoIABx3nY/mh6b+Yq+nUfw==",
    "cf_clearance": "hpxV4fZM8HptNTaEpixG73dBXIZLVfa.a8yAQA9b6jI-1718762520-1.0.1.1-X3VrNFR6oPSzJO4nwHoR6bbjXK8g8r9yny_5BQDdPcemu2vs9hdge2MNs78u3eR6u9u1FOJ9arlKvGtv37NsLA",
    "_ga": "GA1.1.906992827.1718762519",
    "__utmc": "136797536",
    "JSESSIONID": "04DF41D5A2FC6ECB776D9C8BB626F98D"
}

duplicate_list = []
error_list = []
completed_list=[]
data = []
Total_count=None
attachment=None
current_date=None
current_time=None
Ref_value=None
ini_path=None
pdf_count = 1
url_id="76209999"

try:
    with open('completed.txt', 'r', encoding='utf-8') as read_file:
        read_content = read_file.read().split('\n')
except FileNotFoundError:
    with open('completed.txt', 'w', encoding='utf-8'):
        with open('completed.txt', 'r', encoding='utf-8') as read_file:
            read_content = read_file.read().split('\n')


current_datetime = datetime.now()
current_date = str(current_datetime.date())
current_time = current_datetime.strftime("%H:%M:%S")

ini_path = os.path.join(os.getcwd(), "Info.ini")
Download_Path, Email_Sent, Check_duplicate, user_id = common_function.read_ini_file(ini_path)
current_out = common_function.return_current_outfolder(Download_Path, user_id, url_id)
out_excel_file = common_function.output_excel_name(current_out)
Ref_value = "66"

ref_66_download_path = os.path.join(tempfile.gettempdir(), 'ref_66_download')
if not os.path.exists(ref_66_download_path):
    os.makedirs(ref_66_download_path)
driver, init_errors = init_public_driver(ref_66_download_path)

if driver is None:
    print("Driver initiation failed. Errors:", init_errors)
    error_list.extend(init_errors)
    common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list, len(completed_list),ini_path, attachment, current_date, current_time, Ref_value)
else:
    print("Driver initiation success. Success:")

main_link=('https://ajph.aphapublications.org/')
API_KEY = return_api_key()
try:
    soup= get_soup_using_requests(main_link,headers,cookies)
    current_issue_ele=soup.find("div",class_="navContainer").find("ul",class_="subnav").find_all("li")[1].find("a").get("href")
    current_issue_link="https://ajph.aphapublications.org"+current_issue_ele
    current_issue_soup = get_soup_using_requests(current_issue_link,headers,cookies)
    print(current_issue_soup)
    month_year_text=current_issue_soup.find("div",class_="page-heading").find("h1").get_text(strip=True)
    pattern = r'(?P<month>\w+)\s(?P<year>\d{4})'
    match = re.match(pattern, month_year_text)
    if match:
        month = match.group('month')
        year = match.group('year')
    All_articles=current_issue_soup.find_all('div',class_='articleEntry')

    Total_count = len(All_articles)
    print(f"Total number of articles:{Total_count}", "\n")
    article_index, article_check = 0, 0
    while article_index < len(All_articles):
        Article_link = None
        try:
            Article_link = 'https://ajph.aphapublications.org' + All_articles[article_index].find("div",class_="art_title linkable").find('a',class_="ref nowrap").get('href')
            Article_title = All_articles[article_index].find("div",class_="art_title linkable").find('a').find("span",class_="hlFld-Title").text.strip()
            volume_issue_text=All_articles[article_index].find("span",class_="issueInfo").get_text(strip=True)
            pattern = r'(?P<volume>\d+)\((?P<issue>\d+)\)'
            match = re.match(pattern, volume_issue_text)
            if match:
                volume = match.group('volume')
                issue = match.group('issue')
            page_range_text = All_articles[article_index].find("span", class_="articlePageRange").get_text(strip=True)
            patterns = r'pp.\s(?P<page_range>\d+–\d+)'
            page_range_match = re.search(patterns, page_range_text)
            if page_range_match:
                page_range = page_range_match.group('page_range')
            article_soup, cookies = get_driver_content(Article_link, driver)
            doi=article_soup.find("div",class_="article-citation").find("a").get("href").rsplit('doi.org/',1)[-1]
            pdf_link = f'https://ajph.aphapublications.org/doi/pdf/'+doi+"?download=true"
            check_value,tpa_id = common_function.check_duplicate(doi, Article_title, url_id, volume, issue)
            if Check_duplicate.lower() == "true" and check_value:
                message = f"{Article_link} - duplicate record with TPAID : {tpa_id}"
                duplicate_list.append(message)
                print("Duplicate Article :", Article_title)
            else:
                print("Original Article :", Article_title)
                try:
                    pdf_save=os.path.join(current_out,f"{pdf_count}.pdf")
                    get_driver_pdf(pdf_link, pdf_save, ref_66_download_path,driver,error_list)
                    data.append({"Title": Article_title, "DOI": doi, "Publisher Item Type": "", "ItemID": "","Identifier": "","Volume": volume, "Issue": issue,
                                 "Supplement": "", "Part": "","Special Issue": "", "Page Range": page_range, "Month": month, "Day": "","Year": year,
                                 "URL": pdf_link, "SOURCE File Name": f"{pdf_count}.pdf", "user_id": user_id})
                    df = pd.DataFrame(data)
                    df.to_excel(out_excel_file, index=False)
                    pdf_count += 1
                    scrape_message = f"{Article_link}"
                    completed_list.append(scrape_message)
                    with open('completed.txt', 'a', encoding='utf-8') as write_file:
                        write_file.write(Article_link + '\n')
                except Exception as error:
                    message = f"Error link - {Article_link} : {str(error)}"
                    error_list.append(message)
                    print(error)
            article_index, article_check = article_index + 1, 0
        except Exception as error:
            if article_check < 4:
                article_check += 1
            else:
                message = f"Error link - {Article_link} : {str(error)}"
                print("Download failed :", Article_title)
                error_list.append(message)
                article_index, article_check = article_index + 1, 0
    try:
        common_function.sendCountAsPost(url_id, Ref_value, str(Total_count), str(len(completed_list)),str(len(duplicate_list)), str(len(error_list)))
    except Exception as error:
        message = str(error)
        error_list.append(message)
    if str(Email_Sent).lower() == "true":
        attachment_path = out_excel_file
        if os.path.isfile(attachment_path):
            attachment = attachment_path
        else:
            attachment = None
        common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,len(completed_list), ini_path, attachment, current_date,current_time, Ref_value)
    sts_file_path = os.path.join(current_out, 'Completed.sts')
    with open(sts_file_path, 'w') as sts_file:
        pass

except Exception as error:
    Error_message="Error in the site :"+str(error)
    print(Error_message)
    error_list.append(Error_message)
    common_function.attachment_for_email(url_id, duplicate_list, error_list, completed_list,len(completed_list), ini_path, attachment, current_date, current_time,Ref_value)

finally:
    subject, error_html_content = common_function.email_body(current_date, current_time, duplicate_list, error_list,completed_list, len(completed_list), url_id, Ref_value)
    error_file_path = os.path.join(current_out, 'download_details.html')
    with open(error_file_path, 'w', encoding='utf-8') as file:
        file.write(error_html_content)
    print("Error details file saved to:", error_file_path)

if driver is not None:
    driver.quit()
