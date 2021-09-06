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
        'url': "https://voice.baidu.com/act/newpneumonia/newpneumonia",
        'click':"#nationTable > table > thead > tr > th:nth-child(2) > div",
        'element':"xpath=//*[@id='nationTable']/table",
    },
    {
        'filename': "file2",
        'url': "https://voice.baidu.com/act/newpneumonia/newpneumonia",
        'click':"#foreignTable > table > thead > tr > th:nth-child(2) > div",
        'element':"#foreignTable",
    },
]


def run(page,x,i):
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
    timestamp=datetime.now().strftime("%Y%m%dT%H%M%S")
    print(timestamp)
    page.wait_for_selector(x['element'])
    page.click(x["click"])
    time.sleep(0.5)
    dw_path=dw_path + x["filename"] + '__' + timestamp + ".png"
    png_path=png_path + x["filename"]+'_screenshot' + '__' + timestamp + ".png" 
    locals()['ele'+str(i)] = page.query_selector(x["element"])
    locals()['ele'+str(i)] .screenshot(path=png_path)
    locals()['ele'+str(i)] .screenshot(path=dw_path)
 
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://voice.baidu.com/act/newpneumonia/newpneumonia")
    # Open new page
    for i,x in enumerate(files):
        run(page,x,i,)
    with open("message.txt","w") as f:
        tz_utc_8 = timezone(timedelta(hours=8))
        now = datetime.now(tz=tz_utc_8)
        dt = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[Github Action]: {os.path.basename(__file__)} in <{dt}>")
    context.close()
    browser.close()
