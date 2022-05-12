#!/usr/bin/env python3

import os
import re
import sys
from datetime import datetime

import requests
from lxml import html
from requests.exceptions import ConnectionError, HTTPError

GOURMET_URL = 'http://ponavka.gourmetrestaurant.cz/'
MENU_XPATH = '/html/body/div[2]/div/div[2]/div[2]/div/div[1]/ul/li/div[3]/table/tbody/tr'


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


def get_heading():
    todays_date = datetime.today().strftime('%d.%m.%Y')
    return f'**Dnešní menu** ( {todays_date} )\n\n'


def remove_alergens(menu_name):
    return re.sub(r' \*.*$', '', menu_name)


def process_menu_item(menu):
    items = [item.text_content() for item in menu.getchildren()]
    if 'Polévka' in items[0] or 'Menu' in items[0]:
        menu_name = remove_alergens(items[0])
        return f'**{menu_name.strip()}:** {items[1].strip()} ({items[2].strip()})\n\n'


def prepare_data(menus):
    menu_items = [process_menu_item(menu) for menu in menus]
    menu_items = [item for item in menu_items if item is not None]
    heading = get_heading()
    return ''.join([heading] + menu_items)


if __name__ == '__main__':
    if 'MM_GOURMET_URL' not in os.environ:
        print('MM_GOURMET_URL not set')
        sys.exit(1)
    try:
        page = get_page_content()
        menus = get_menu(page)
        data = prepare_data(menus)
        message_data = {
            'text': data
        }
        mm_gourmet_url = os.environ['MM_GOURMET_URL']
        response = requests.post(mm_gourmet_url, json=message_data)
        response.raise_for_status()
    except ConnectionError as e:
        print('Could not connect to mattermost')
        sys.exit(1)
    except HTTPError as e:
        print(e)
        sys.exit(1)
