import re
import requests
import datetime
from json.decoder import JSONDecodeError


API_DOMAIN = 'https://rasp.dmami.ru/'

def get_data(group: str):
    '''Gets the schedule from the server

    Keyword arguments:
    group -- defines the student group for which to get the schedule
    '''

    cookies = {
        'bpc': get_bpc(),
        'group': group
    }
    headers = {'referer': API_DOMAIN }
    gateway = f'{API_DOMAIN}site/group?group={group}&session=0'
    result = requests.post(gateway, cookies=cookies, headers=headers)
    try:
        data = result.json()['grid']
    except JSONDecodeError:
        return False
    else:
        return data


def get_bpc():
    '''Sends n̶u̶d̶e̶s̶ an empty request to receive cookies'''

    responce = requests.get(API_DOMAIN).text
    return re.search(r'(?<=bpc\=).*(?=\;Path)', responce).group(0)

if __name__ == '__main__':
    print(get_data('181-362'))