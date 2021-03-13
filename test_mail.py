from utils import send_mail
import sys, json
from email_theme import body_html
import pandas as pd
from sqlalchemy import create_engine
from pretty_html_table import build_table
import sys
import os
from datetime import datetime
import emoji




Pinsta_username = 'waiting4_wind'
BotProcess = 14
Pbot_id = 1
Pemail='kdresdell@gmail.com'
Ptags = 'Kiteboarding'

Pcomments = 'Nice :thumbsup:'
Pcomments = emoji.emojize(Pcomments, use_aliases=True)



##
## UPDATE DATABASE INFO
##

from app import db, Bot, UserInfo

bot = Bot.query.filter_by(id=Pbot_id).first()
bot.status = 'Finished'
bot.end_dt = datetime.now()
CCYYMMDD = datetime.now().strftime("%Y-%m-%d")

##
## SEND EMAIL REPORT
##

record_file = "/home/kdresdell/Documents/InstaPy/logs/{}/recordActivity.json".format(Pinsta_username)

with open(record_file) as f:
    data = json.load(f)

d1 = data[Pinsta_username][CCYYMMDD]
d2 = sorted(d1.keys())

Rlikes = 0
Rcomments = 0
Rfollows = 0
Runfollows = 0
Rserver_calls = 0

for i in d2:
    Rlikes = Rlikes + d1[i]['likes']
    Rcomments = Rcomments + d1[i]['comments']
    Rfollows = Rfollows + d1[i]['follows']
    Runfollows = Runfollows + d1[i]['unfollows']
    Rserver_calls = Rserver_calls + d1[i]['server_calls']


# SAVING D3 IN BOT DATA BASE
bot.results = d1
db.session.commit()

Pcomments = emoji.emojize(Pcomments, use_aliases=True)

message = """Hi <b>{}</b>, <br><br>
             Your Insta@bot just finished his work after {} minutes <br><br>
             Here are the high level statistics for ( {} ) :  <br>
             <ul>
              <li> Searched #tags : <b>{}</b>   </li>
              <li> Your comments  : <b>{}</b>   </li>
            </ul>
            <table style="margin-left: 1.4cm;">
            <thead>
              <tr>
                <th style="text-align:center">
                  <img src="https://drive.google.com/uc?export=view&id=11BRBCAWdMJ5WRc_41-mmHSoJqMeSLvII" alt="" width="50" border="0" style="border:0; outline:none; text-decoration:none; display:block;">
                </th>
                <th style="text-align:center">
                   <img src="https://drive.google.com/uc?export=view&id=1wFAn2Wu14d-6k-YN1RXXRFTlvwuod1lN" alt="" width="50" border="0" style="border:0; outline:none; text-decoration:none; display:block;">
                </th>
                <th style="text-align:center">
                   <img src="https://drive.google.com/uc?export=view&id=1BqnnjbwFTtRZ8NQKts4xfJBxhKI7h-Xw" alt="" width="50" border="0" style="border:0; outline:none; text-decoration:none; display:block;">
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="text-align:center; font-size:30px">{}</td>
                <td style="text-align:center; font-size:30px">{}</td>
                <td style="text-align:center; font-size:30px">{}</td>
              </tr>

            </tbody>
            </table>

            <br>
            Find attached, log file and some screenshots of your bot at work &#128518;
            <br><br>
            Thanks for using our service ! <br><br>

            Ken<br>
            kdresdell@gmail.com""".format(Pinsta_username, BotProcess, CCYYMMDD, Ptags, Pcomments,
                                           Rlikes, Rcomments, Rfollows )


body  = body_html.replace("{{HTML_TO_REPLACE}}" , message)

file_list = [ r'/home/kdresdell/Documents/InstaPy/logs/{}/screenshot_1.png'.format(Pinsta_username) ,
              r'/home/kdresdell/Documents/InstaPy/logs/{}/screenshot_2.png'.format(Pinsta_username) ,
              r'/home/kdresdell/Documents/InstaPy/logs/{}/screenshot_3.png'.format(Pinsta_username) ,
              r'/home/kdresdell/Documents/InstaPy/logs/{}/general.log'.format(Pinsta_username) ,
            ]

send_mail([Pemail], 'Your Inst@Bot process is done...', body, file_list)
