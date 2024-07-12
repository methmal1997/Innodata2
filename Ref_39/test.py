import requests


def get_session():
    logi_url='https://www.edimark.fr'
    new_session=requests.session()
    session_login=new_session.get(logi_url)
    login_post ='https://www.edimark.fr/connexion'

    payload={'redirect': 'https://www.edimark.fr/',
    'email': 'bd-scm@elsevier.com',
    'password':'10739840',
    'persist':'1'}

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Length' : '96',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.edimark.fr',
        'Origin': 'https://www.edimark.fr',
        'Priority' : 'u=1',
        'Referer': 'https://www.edimark.fr/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'X-Requested-With': 'XMLHttpRequest'
    }

    response=new_session.post(login_post,data=payload,headers=headers)
    return new_session

new_session = get_session()
response = new_session.get('https://www.edimark.fr')
print(response.content)