#!/usr/bin/env python
# coding=utf-8
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta, timezone
import time
import os
import re


files = [
    {
        'filename': "file1",
        'url': "https://github.com/trending",
        'element':"#js-pjax-container > div.position-relative.container-lg.p-responsive.pt-6 > div"
    },
]

def run(p,x):
    """
    init some variable
    """
    try:
        png_path="./screenshot/"  
        os.mkdir(png_path)
    except Exception as e:
        pass

    try:
        dw_path="./download/"
        os.mkdir(dw_path)
    except Exception as e:
        pass

    message_path="./message.txt"  
    timestamp=datetime.now().strftime("%Y%m%dT%H%M%S")
    print(timestamp)

    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    page.goto(x['url'])
    page.wait_for_selector(x["element"])
    dw_path=dw_path + x["filename"] + '__' + timestamp + ".png"
    png_path=png_path + x["filename"]+'_screenshot' + '__' + timestamp + ".png" 
    element_handle = page.query_selector(x["element"])
    element_handle.screenshot(path=png_path)
    element_handle.screenshot(path=dw_path)

    with open(message_path,'w') as f:
        tz_utc_8 = timezone(timedelta(hours=8))
        now = datetime.now(tz=tz_utc_8)
        dt = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[Github Action]: {os.path.basename(__file__)} in <{dt}>\n{x['url']}")
 
    context.close()
    browser.close()

with sync_playwright() as p:
    for x in files:
        run(p,x)
