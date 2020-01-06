#!/usr/bin/env python3

from lxml import html
from datetime import datetime
import requests
from requests.exceptions import ConnectionError, HTTPError
import json
import sys
import re
import os

GOURMET_URL='http://ponavka.gourmetrestaurant.cz/'
MENU_XPATH='/html/body/div[2]/div/div[2]/div[2]/div/div[1]/ul/li/div[3]/div/table/tbody/tr'

def get_page_content():
    try:
        page = requests.get(GOURMET_URL)
        page.raise_for_status()
        return page
    except ConnectionError as e:
        print('Could not connect to gourmet')
        sys.exit(1)
    except HTTPError as e:
        print(e)
        sys.exit(1)

def get_menu(page):
    tree = html.fromstring(page.content)
    menus = tree.xpath(MENU_XPATH)
    if len(menus) == 0:
        print('Could not find menu')
        sys.exit(1)
    return menus

def get_block(text): 
    return {'type': 'section', 'text': {'type': 'mrkdwn', 'text': text}}

def get_heading():
    todays_date = datetime.today().strftime('%d.%m.%Y')
    heading = f'*Dnešní menu* ( {todays_date} )'
    return get_block(heading)

def remove_alergens(menu_name):
    return re.sub(r' \*.*$', '', menu_name)

def process_menu_item(menu):
    items = [item.text for item in menu.getchildren()]
    menu_name = remove_alergens(items[0])
    menu_item = f'*{menu_name}:* {items[1]} ({items[2]})'
    return get_block(menu_item)

def prepare_data(menus):
    menu_items = [process_menu_item(menu) for menu in menus]
    heading = get_heading()
    return {'blocks': [heading] + menu_items}
    

if __name__ == '__main__':
    if 'SLACK_GOURMET_URL' not in os.environ:
        print('SLACK_GOURMET_URL not set')
        sys.exit(1)
    page = get_page_content()
    menus = get_menu(page)
    try:
        slack_url = os.environ['SLACK_GOURMET_URL']
        response = requests.post(slack_url, json=prepare_data(menus))
        response.raise_for_status()
    except ConnectionError as e:
        print('Could not connect to slack')
        sys.exit(1)
    except HTTPError as e:
        print(e)
        sys.exit(1)

