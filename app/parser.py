import re
import requests
import datetime


API_DOMAIN = 'https://rasp.dmami.ru/'

def get_bpc():
    responce = requests.get(API_DOMAIN).text
    return re.search(r'(?<=bpc\=).*(?=\;Path)', responce).group(0)

def get_data(group: str):
    cookies = {
        'bpc': get_bpc(),
        'group': group
    }
    headers = {'referer': API_DOMAIN }
    gateway = f'{API_DOMAIN}site/group?group={group}&session=0'
    return requests.post(gateway, cookies=cookies, headers=headers).json()['grid']
    

if __name__ == '__main__':
    data = get_data('181-362')
    print(data)
    print(data.keys())