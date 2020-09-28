#!/usr/bin/env python3
import subprocess
import requests
from bs4 import BeautifulSoup
import json
from sys import argv, exit

try:
    argv[1]
except IndexError:
    print("Введите ID кастомера: get_tickets.py 2343322")  
    exit()


def read_token():
    with open('tmp.tok', 'r') as f:
        token = f.read()
        token_dict = json.loads(token)
        token_raw = token_dict.get('token')
    return token_raw

def get_token():
    login = input('LDAP login: ')
    password =  input('Password: ')
    r = requests.post('https://enter.beget.ru/login', cookies = {'_ym_uid': '1594184324705932085', '_ym_d':'1597036142', '_ga':'GA1.2.1258639406.1597345883',\
        'experimentation_subject_id':'IjhmYTQ0ZDc0LWE5MDktNGMxMi1hOGMxLWIwN2MwZDRmNzBhOCI%3D--9279cf1c4ce8acb081d06f22fdc11ed9790a280d',\
        '_ym_isad':'1'}, data = {'login':login, 'password':password})
    with open ('tmp.tok', 'w') as f:
            f.write(str(r.text))

def get_tickets():
    r = requests.post(url+str(customer_id), cookies = cookies, params = params)
    with open ('result.html', 'w') as file:
        file.write(r.text)
    with open ('result.html', 'r') as file:
        cust_page = file.read()
    return cust_page

try:
    read_token()
except IOError:
    get_token()

token_raw = read_token()

url = 'https://hp.beget.ru/customerinfo'

try:
    customer_id = int(argv[1])
except IndexError:
    print('Введите ID кастомера: get_tickets.py 2343322')
    exit()

cookies = {'begetInnerJWT': token_raw }
params = {'ajaxj':'', 'method': 'ajaxj_get_customer_tickets'}

cust_page = get_tickets()



soup = BeautifulSoup(cust_page, "html.parser")
tikets_data = soup.text
try:
    tickets_dict = json.loads(tikets_data)
except json.decoder.JSONDecodeError:
    print("Токен протух, надо обновить")
    get_token()
    cust_page = get_tickets()

tickets_all = tickets_dict.get('tickets')
count = 3
for el in tickets_all:
#    print(el)
    if count > 0:
        print('https://hp.beget.ru/helpdesk/ticket/' + str(el.get('id')), el.get('subject'))
        count -= 1
    else:
        break

