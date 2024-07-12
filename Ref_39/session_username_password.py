import requests
import os
from bs4 import BeautifulSoup

out_path='Out'
if not os.path.exists(out_path):
    os.makedirs(out_path)
out_folder=os.path.join(out_path,'New.pdf')

new_session = requests.session()
url = 'https://www.edimark.fr'

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


new_session.get(url,headers=mainHeaders)

post_url='https://www.edimark.fr/connexion'

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

s = new_session.post(post_url,data=data,headers=loginHeaders).content
print(s)


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

new_session.get("https://www.edimark.fr/",headers=lastHeader)

# soup=new_session.get("https://www.edimark.fr/revues/medecine-et-enfance/volume-44-numero-3/quelle-alimentation-pour-ladolescent-sportif").content

# soup=BeautifulSoup(soup,"html.parser")
# print(soup)


