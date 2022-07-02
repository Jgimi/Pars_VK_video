import requests
from bs4 import BeautifulSoup
import json
import xml
from xml.etree import ElementTree
import csv
import os
from datetime import datetime
import pandas as pd
import re
import os.path


cookies = {
    'remixlang': '0',
    'remixstid': '2129592203_2lOXPN6hM02yRlAoepOn8kvEOCiJWcxqyqX4yEYKfzX',
    'remixscreen_dpr': '1',
    'remixscreen_depth': '24',
    'remixdt': '0',
    'tmr_lvid': '269c1f49882fd71427dee45a9b468e10',
    'tmr_lvidTS': '1636133354599',
    'remixuas': 'ZjU0MWE0ZDJmZGMxNjgxMTVmNjU1MjA5',
    'remixluas2': 'YTY2NzhiNGRiMDFiNDIxM2JlMjA3M2Jl',
    'remixflash': '0.0.0',
    'remixscreen_width': '1920',
    'remixscreen_height': '1080',
    'remixdark_color_scheme': '0',
    'remixcolor_scheme_mode': 'auto',
    'remixstlid': '9100438374497749946_xU1xadhA6PQMfHe2kvfFKqt0fV1uF1tTPk6UXpWG5oL',
    'remixscreen_orient': '1',
    'remixgp': '2783ddd0feb929da281ef79c69f1bdee',
    'remixnsid': 'vk1.a.Wj7KSZ_eNgLT_yYh_NBGVSUXl8NhUl9BVM1YDEAskWcVLu_MzjZCvza_Yyeswc2_t4-D_1eQTRlMtTC81TtWV9THqpJYY5R_bN2ztrMDshHl2V5hyuxKwKo5x6ojb_U0IqiUZ8p_tFuJ7N2wuhxnBpU5TI1q5L_26TWVUIT6d0F7Fu0Tc8ZZNobEk-yFu8Gj',
    'remixsid': '1_2Ss9oJ1XR7-GS-eRxOKvJ9_7ZDH6xWqNNEbc5qqRbdLb4qNu31C9NUb-LgNZ4mjMnLQfB7FTm6LD74l1VratsA',
    'remixlgck': '0fcc59f4ec53dd7a7a',
    'remixrefkey': '2ce9595bb4c942d6ed',
    'remixscreen_winzoom': '1',
    'remixua': '41%7C-1%7C194%7C767779896',
    'tmr_detect': '1%7C1656151109418',
    'tmr_reqNum': '141',
}

headers = {
    'authority': 'vk.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'remixlang=0; remixstid=2129592203_2lOXPN6hM02yRlAoepOn8kvEOCiJWcxqyqX4yEYKfzX; remixscreen_dpr=1; remixscreen_depth=24; remixdt=0; tmr_lvid=269c1f49882fd71427dee45a9b468e10; tmr_lvidTS=1636133354599; remixuas=ZjU0MWE0ZDJmZGMxNjgxMTVmNjU1MjA5; remixluas2=YTY2NzhiNGRiMDFiNDIxM2JlMjA3M2Jl; remixflash=0.0.0; remixscreen_width=1920; remixscreen_height=1080; remixdark_color_scheme=0; remixcolor_scheme_mode=auto; remixstlid=9100438374497749946_xU1xadhA6PQMfHe2kvfFKqt0fV1uF1tTPk6UXpWG5oL; remixscreen_orient=1; remixgp=2783ddd0feb929da281ef79c69f1bdee; remixnsid=vk1.a.Wj7KSZ_eNgLT_yYh_NBGVSUXl8NhUl9BVM1YDEAskWcVLu_MzjZCvza_Yyeswc2_t4-D_1eQTRlMtTC81TtWV9THqpJYY5R_bN2ztrMDshHl2V5hyuxKwKo5x6ojb_U0IqiUZ8p_tFuJ7N2wuhxnBpU5TI1q5L_26TWVUIT6d0F7Fu0Tc8ZZNobEk-yFu8Gj; remixsid=1_2Ss9oJ1XR7-GS-eRxOKvJ9_7ZDH6xWqNNEbc5qqRbdLb4qNu31C9NUb-LgNZ4mjMnLQfB7FTm6LD74l1VratsA; remixlgck=0fcc59f4ec53dd7a7a; remixrefkey=2ce9595bb4c942d6ed; remixscreen_winzoom=1; remixua=41%7C-1%7C194%7C767779896; tmr_detect=1%7C1656151109418; tmr_reqNum=141',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

group = input('Введите группу:')

# 'https://vk.com/video/@mudakoff'
response = requests.get(group, cookies=cookies, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
raw_data = soup.find('div', class_='ge_video_pane video_subtab_pane_uploaded VideoPane').find_all('div', class_=re.compile('_video_item ge_video_item_'))


id_name_scr = {}


for i in raw_data:
    video_id = i["data-id"]
    video_name = i.find('img').get('alt').strip()
    video_href = i['data-thumb']
    # img = requests.get(video_href)
    # with open(f'{video_id[1:]}_{video_name}.webp', 'wb') as file:
    #     file.write(img.content)
    # img_name = f'{video_id[1:]}_{video_name}.webp'
    id_name_scr[video_id[1:]] = {'name':video_name, 'href': video_href}

with open('data.json', 'w') as outfile:
    json.dump(id_name_scr,outfile, ensure_ascii=False, indent=4)

