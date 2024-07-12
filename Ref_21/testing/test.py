import requests

headers2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded"
}


# pdf_link_id = "e458d321-7387-4870-bd27-b8bdfee1f6f8"
# Pdf_link = f"http://www.ysxb.ac.cn/en/data/article/check-article-pdf?id={pdf_link_id}"
# url = "http://www.ysxb.ac.cn/en/data/article/export-pdf"
# payload = {
#     "id": pdf_link_id
# }
# response_2 = requests.post(url, data=payload)
# # print(response_2.status_code)
# # print(response_2.content)

pdf_link_id = "8a29eb99-40c1-4862-94d5-798d41384d37"
Pdf_link = f"http://www.ysxb.ac.cn/en/data/article/check-article-pdf?id={pdf_link_id}"
url_download = "http://www.ysxb.ac.cn/en/data/article/export-pdf"
url_check = "http://www.ysxb.ac.cn/en/data/article/check-article-pdf"
payload = {
    "id": pdf_link_id
}


response_check = requests.post(url_check, data=payload)
if response_check.status_code == 200:
    json_response = response_check.json()
    if json_response.get("result") == "success":
        print("PDF file exists. Proceeding to download...")
        response_2 = requests.post(url_download, data=payload, headers=headers2)
        # print(response_2.content)