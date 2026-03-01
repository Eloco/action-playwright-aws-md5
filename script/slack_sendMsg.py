#!/usr/bin/env python
# coding=utf-8

import requests
import os
import json
import time
import random

msgPath=os.environ.get("msgPath")
hook=os.environ.get("Hook")
secHook=os.environ.get("secHook")


def send_slack_message(payload, webhook):
    """Send a Slack message to a channel via a webhook. 
    
    Args:
        payload (dict): Dictionary containing Slack message, i.e. {"text": "This is a test"}
        webhook (str): Full Slack webhook URL for your chosen channel. 
    
    Returns:
        HTTP response code, i.e. <Response [503]>
    """
    return requests.post(webhook, json.dumps(payload))

slackHook=f"https://hooks.slack.com/services/{secHook}/{hook}"

if os.path.exists(msgPath):
    if os.path.isdir(msgPath):
        for msg in os.listdir(msgPath):
            path = os.path.join(msgPath,msg)
            m= open(path,"r").read()
            payload = {"text": m }
            while not send_slack_message(payload, slackHook):
                time.sleep(random.randint(5,10))
            time.sleep(random.randint(2,5))
    elif os.path.isfile(msgPath):
        m= open(msgPath,"r").read()
        payload = {"text": m }
        while not send_slack_message(payload, slackHook):
            time.sleep(random.randint(5,10))
