# -*- coding: utf-8 -*
import pyMail as mailUtils
from jieba.analyse import *
import html2text
import os

def takeSecond(elem):
    return elem[1]

def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

try:
    os.mkdir("download")
except:pass

mail_user        =os.environ.get('MAIL_USER')
mail_pass        =os.environ.get('MAIL_PASS')
mail_server      =os.environ.get('MAIL_SERVER')
mail_box         =os.environ.get('MAIL_BOX')

rml = mailUtils.ReceiveMailDealer(mail_user,mail_pass,mail_server)
for f in rml.showFolders()[1]:
    print(f.decode('gbk'))
rml.select(mail_box)
h = html2text.HTML2Text()
h.ignore_links=True
for num in mailUtils.muti_decode(rml.getToday()[1][0]).split(' ')[-10:]:
    print(num)
    if num != '':   
        mailInfo = rml.getMailInfo(str(num))
        with open(f"download/{num}.txt","w") as f:
            msg=""
            msg+=f""":mailbox: [Github action] \t <{mail_user}>\n"""
            msg+=f"""[subject]:\t{mailInfo['subject']}\n"""
            msg+=f"""[from]:\t\t{" ".join(mailInfo['from'])}\n"""
            msg+=f"""[to]:\t\t{  " ".join(mailInfo['to'  ])}\n"""
            if type(mailInfo['body'])==str:
                msg+="<keyword>:\t"
                html_text=h.handle(mailInfo['body'])
                keyword_list=[]
                for keyword, weight in extract_tags(html_text, withWeight=True):
                    if is_contains_chinese(keyword):
                        weight+=0.5
                    keyword_list.append([keyword,weight])
                keyword_list.sort(key=takeSecond,reverse=True)
                for k in keyword_list[0:5]:
                    msg+=f"{k[0]}  "
            f.write(msg)
