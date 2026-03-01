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
        'url': "http://www.weather.com.cn/weather1d/10102010008A.shtml",
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
    timestamp=datetime.now().strftime("%Y%m%dT%H%M%S")
    print(timestamp)

    browser = p.firefox.launch(headless=True)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    page.goto(x['url'])
    dw_path=dw_path + x["filename"] + '__' + timestamp + ".png"
    png_path=png_path + x["filename"]+'_screenshot' + '__' + timestamp + ".png"
    element_handle = page.query_selector("body > div.con.today.clearfix > div.left.fl")
    element_handle.screenshot(path=png_path)
    element_handle.screenshot(path=dw_path)

    context.close()
    browser.close()

with sync_playwright() as p:
    for x in files:
        run(p,x)
    with open("message.txt","w") as f:
        tz_utc_8 = timezone(timedelta(hours=8))
        now = datetime.now(tz=tz_utc_8)
        dt = now.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[Github Action]: {os.path.basename(__file__)} in <{dt}>")
