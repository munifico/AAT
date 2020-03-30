# import requests
# import json
#
# web_hook_url = 'https://hooks.slack.com/services/THE_REST_OF_MY_APPS_URL' # Need to encrypt this value in future
#
# slack_msg = {'text': 'Alert from Python'}
#
# requests.post(web_hook_url, data=json.dumps(slack_msg))

from slacker import Slacker
import requests
from bs4 import BeautifulSoup
import os

slack_token = "xoxb-1031024079200-1037160759654-WcC4fT9pVtV2GdLLXwBBmvfF"
slack = Slacker(slack_token)
ch = "#aat-graduation-work"

req = requests.get('https://blex.me/@mildsalmon/series/%EC%A1%B8%EC%97%85%EC%9E%91%ED%92%88-aat')

html = req.text
soup = BeautifulSoup(html, 'xml')
posts = soup.select('div > h5 > a')
posts_num = len(posts)
posts_num = str(posts_num)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not(os.path.isfile(os.path.join(BASE_DIR, 'blex_posts_num.txt'))):
    with open(os.path.join(BASE_DIR, 'blex_posts_num.txt'), 'w+', encoding='utf-8') as f_write:
        f_write.writelines(posts_num)

with open(os.path.join(BASE_DIR, 'blex_posts_num.txt'), 'r+', encoding='utf-8') as f_read:
    before = f_read.readline()
    # print(posts[int(posts_num)-1].get('href'))  # 솔직히 이건 너무 대충 만든거긴 하다
    if posts_num > before:
        url = "https://blex.me" + posts[int(posts_num)-1].get('href')
        slack.chat.post_message(channel=ch, text="AAT 관련 새 글이 있습니다 !")
        slack.chat.post_message(channel=ch, text=posts[int(posts_num)-1].text)
        slack.chat.post_message(channel=ch, text=url)
        print("최신글 있ㅎ음")
    elif posts_num == before:
        print("같음\n")

with open(os.path.join(BASE_DIR, 'blex_posts_num.txt'), 'w+', encoding='utf-8') as f_write:
    f_write.writelines(str(posts_num))

# slack.chat.post_message(channel=ch, text="https://blex.me"+posts[int(posts_num)-1].get('href'), unfurl_links=True, unfurl_media=True,mrkdwn=False)
#                         blocks=[
#                                     {
#                                         "type": "section",
#                                         # "pretext": "hi",
#                                         "text": {"type": "plain_text", "text": "https://blex/" }#+ posts[int(posts_num)-1].get('href')}
# #
#                                     }
#                                 ])
# https://blex.me/@mildsalmon/aat_phase-2-make-main-window-and-automatic-start
# print(posts[int(posts_num)-1].get('href'))