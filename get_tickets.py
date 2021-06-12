#!/usr/bin/env python3
import subprocess
import requests
from bs4 import BeautifulSoup
import json
from sys import argv, exit

url = 'https://hp.beget.ru/customerinfo'
url_main = 'https://hp.beget.ru/main'
params = {'ajaxj':'', 'method': 'ajaxj_get_customer_tickets'}
params_for_id = {'ajaxj':'', 'method': 'ajaxj_search_client_widget'}


try:
    argv[1]
except IndexError:
    print("Введите ID кастомера или его логин: get_tickets.py 2343322")  
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
    with open ('result.json', 'w') as file:
        file.write(r.text)
    with open ('result.json', 'r') as file:
        cust_page = file.read()
    return cust_page

def is_login(string):
    return any(char.isalpha() for char in string)

def get_id(customer):
    r = requests.post(url_main, cookies = cookies, params = params_for_id, data = {'search_str':customer + '!'})
    return r


try:
    read_token()
except IOError:
    get_token()


token_raw = read_token()
cookies = {'begetInnerJWT': token_raw }
customer = argv[1]


if is_login(argv[1]):
    try:
        customer_id = get_id(customer).json()[0].get('id')
    except IndexError:
        print("По логину не найдено, попробуй по ID")
        exit()
else:
    customer_id = argv[1]

cust_page = get_tickets()
soup = BeautifulSoup(cust_page, "html.parser")
tikets_data = soup.text


try:
    tickets_dict = json.loads(tikets_data)
except json.decoder.JSONDecodeError:
    print("Токен протух, надо обновить")
    get_token()
    cust_page = get_tickets()

if tickets_dict.get('tickets') == []:
    print("Неверный ID, или клиент не написал ни одного тикета.")

tickets_all = tickets_dict.get('tickets')
count = 3
for el in tickets_all:
    if count > 0:
        print('https://hp.beget.ru/helpdesk/ticket/' + str(el.get('id')), el.get('subject'))
        count -= 1
    else:
        break

