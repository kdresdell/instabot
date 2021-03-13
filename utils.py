import requests
import sys
from email_theme import body_html
import json
import os
import time
from datetime import datetime
import shutil
import emoji



def send_mail(users_list, subject, body, filenames):

    import smtplib
    import ssl
    from email.mime.text import MIMEText
    from email.utils import formataddr
    from email.mime.multipart import MIMEMultipart  # New line
    from email.mime.base import MIMEBase  # New line
    from email import encoders  # New line

    sender_email = 'kdresdell@gmail.com'
    sender_name = 'Ken Dresdell'
    password = 'qrhdxfkqezpdmlbz'


    msg = MIMEMultipart()
    msg['To'] = ", ".join(users_list)
    msg['From'] = formataddr((sender_name, sender_email))
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    if filenames is not None:
        # If we have attched files list
        for i in filenames:

            try:
                # Open PDF file in binary mode
                with open(i, "rb") as attachment:
                          part = MIMEBase("application", "octet-stream")
                          part.set_payload(attachment.read())

                encoders.encode_base64(part)

                # Add header as key/value pair to attachment part
                part.add_header("Content-Disposition",
                                f"attachment; filename= {i}",)

                msg.attach(part)

            except Exception as e:
                print(f'Oh no! We didn t found the attachment!n{e}')


    try:

        server = smtplib.SMTP('smtp.gmail.com', 587)
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, users_list, msg.as_string())

    except Exception as e:
        print(f'Oh no! Something bad happened!n{e}')


    finally:
        server.quit()







def run_instapy_bot(Pemail, Pinsta_username, Pinsta_password, Ptags, Pcomments, Pmedia, Pbot_id ):

    from instapy import InstaPy
    from instapy import smart_run
    from instapy import set_workspace
    # sudo apt install firefox-geckodriver

    # Start timer for the email report
    start = time.time()

    # First you need to delete user folder
    # if exist

    dir_path = '/home/kdresdell/Documents/InstaPy/logs/{}'.format(Pinsta_username)

    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


    browser = r'/home/kdresdell/Document/geckodriver'
    set_workspace(path="/home/kdresdell/Documents/")

    # get an InstaPy session!
    session = InstaPy(username=Pinsta_username,
                      password=Pinsta_password,
                      headless_browser=True)


    try:
        # starting the try
        with smart_run(session):

            #settings -https://instapy.org/settings/
            session.set_do_follow(True, percentage=10)
            session.set_do_comment(True, percentage=50)
            session.set_comments([Pcomments])
            #session.set_comments(['Nice shot! @{}'], media='Photo')

            session.set_quota_supervisor(enabled=True, sleep_after=["likes", "comments_d", "follows", "unfollows", "server_calls_h"],
                                         sleepyhead=True, stochastic_flow=True, notify_me=True,
                                         peak_likes_hourly=57,
                                         peak_likes_daily=585,
                                         peak_comments_hourly=21,
                                         peak_comments_daily=182,
                                         peak_follows_hourly=48,
                                         peak_follows_daily=None,
                                         # peak_unfollows_hourly=35,
                                         # peak_unfollows_daily=402,
                                         peak_server_calls_hourly=None,
                                         peak_server_calls_daily=4700)

            session.set_relationship_bounds(enabled=True,
                                            delimit_by_numbers=True,
                                            max_followers=5000,
                                            min_followers=100,
                                            min_following=100)

            session.set_do_like(enabled=True, percentage=100)

            # session.set_user_interact(amount=1, randomize=True, percentage=25, media="Photo")

            #session.set_smart_hashtags(['kitesurf', 'snowboard'], limit=3, sort='top', log_tags=True)
            #session.like_by_tags(amount=5, use_smart_hashtags=True)

            # Use_smart_location_hashtags activates like_by_tag to use smart hashtags
            #session.set_smart_location_hashtags(['c294477/levis-canada/'], radius=100, limit=10)
            #session.like_by_tags(amount=10, use_smart_location_hashtags=True)

            #activity
            session.like_by_tags([ Ptags ], amount=500, interact=False)




        # Stop de timer
        stop = time.time()
        BotProcess = round((stop - start)/60)


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







    except Exception as e:
        print(f'Oh no! Something bad happened!n{e}')
        # log error in web page and db
        # send email for credit link
        from app import db, Bot, UserInfo
        bot = Bot.query.filter_by(id=Pbot_id).first()
        bot.status = 'FAILED'
        db.session.commit()

        body = """Hi something went wrong ({}) with your bot retry or click the linkg for a refund...""".format(e)

        send_mail([Pemail],
                   'Something went wrong with your Inst@Bot...pleasse click the link to be refund',
                   body, None )
