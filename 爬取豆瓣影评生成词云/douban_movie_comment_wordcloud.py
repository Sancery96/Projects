import random
import re
import time
import os
from pathlib import Path
import imageio
import jieba.analyse
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np


def get_movie_links(start_url, headers):
    web_data = requests.get(start_url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    movies = soup.find_all('li', class_='list-item')
    movie_list = []
    for item in movies:
        movie = {
            'title': item['data-title'],
            'id': item['id'],
            'link': item.find('a')['href']
        }
        # print(movie)
        movie_list.append(movie)
    return movie_list


def get_movie_comment(id, headers):
    url = f'https://movie.douban.com/subject/{id}/comments'
    comment_list = []
    for i in range(100):
        params = {
                'start': i*20,
                'limit': 20,
                'status': 'P',
                'sort': 'new_score',
        }
        web_data = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(web_data.text, 'lxml')
        comments = soup.find_all('div', class_='comment')
        if comments:
            for item in comments:
                comment = item.find('span', class_='short')
                comment = re.sub(r'[\s]+', '', comment.text, re.S)
                # print(comment)
                comment_list.append(comment)
        else:
            break
    return ''.join(comment_list)

def get_comments(url, headers):
    for movie in get_movie_links(url, headers):
        id = movie['id']
        get_movie_comment(id, headers)
        time.sleep(3)


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


def wordcloud(movie_title, wordstr):
    jieba.analyse.set_stop_words(r'stopwords/cn_stopwords.txt')
    tags = jieba.analyse.extract_tags(wordstr, topK=50, withWeight=True)
    tags = dict(tags)

    bg_pic = np.array(Image.open(os.path.join(Path(__file__).resolve().parent, "snowman.png")))
    cloud = WordCloud(background_color='black', mask=bg_pic, font_path='simhei.ttf', max_font_size=80)
    word_frequence = tags
    myword = cloud.fit_words(word_frequence)
    plt.imshow(myword)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title(movie_title)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    start_url = 'https://movie.douban.com/cinema/nowplaying/beijing/'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Cookie':'bid=FmCsV1DrVTs; ll="108304"; gr_user_id=a720e295-c253-415a-ba72-cfd883cc1855; viewed="4822685"; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=DD3F87CF6DD2320762E2BDAE899123DDD|88261b96e609e137741731695ab9870d; dbcl2="209273357:r+jbUMNOBgo"; ck=YSKe; _pk_ref.100001.4cf6=["","",1622901955,"https://accounts.douban.com/"]; _pk_ses.100001.4cf6=*; __utma=30149280.96046146.1621929586.1622892192.1622901955.11; __utmb=30149280.0.10.1622901955; __utmz=30149280.1622901955.11.4.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1335778629.1621929586.1622892192.1622901955.8; __utmb=223695111.0.10.1622901955; __utmz=223695111.1622901955.8.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=d261414918775fd1.1621929585.8.1622901975.1622892220.'
    }
    # get_comments(start_url, headers)
    # for movie in get_movie_links(start_url, headers):
    #     print(movie)
    movie = get_movie_links(start_url, headers)[0]
    comment = get_movie_comment(movie['id'], headers)
    wordcloud(str(movie['title']), comment)

    print(Path(__file__).resolve().parent)
