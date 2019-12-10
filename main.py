#!/usr/bin/env python
# coding: utf-8

import os
import youtube_dl
import requests
import datetime
import pandas

# consts
VIDEO_DIR = os.path.join(os.getcwd(), "videos")
download_options = {
    "outtmpl": "{VIDEO_DIR}/%(title)s.mp4".format(VIDEO_DIR=VIDEO_DIR)
}

youtube_options = {
    'key': 'APIキー',  # 取得したAPIキー
    'channelId': 'UCCVwhI5trmaSxfcze_Ovzfw',
    'part': 'id,snippet',
    'type': 'video',  # 検索結果を動画のみにする
    'publishedAfter': (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%dT00:00:00Z'),
}


# ローカルのcsvファイルよりダウンロード対象のチャンネルを取得する
def search_channel_list():
    csv_input = pandas.read_csv('data/channellist.csv', encoding='cp932')
    channel_list = list(csv_input.iloc[:, 1])
    return channel_list


# チャンネルidから直近1日分の動画id取得
def search_movie(channel_list):
    id = list()
    for channel in channel_list:
        youtube_options['channelId'] = channel
        r = requests.get('https://www.googleapis.com/youtube/v3/search', params=youtube_options)
        print(r.url)
        data = r.json()
        for item in data['items']:
            print('---------------')
            print('チャンネル名:', item['snippet']['channelTitle'].encode('shift_jis', errors='ignore').decode('shift_jis'))
            print('タイトル:', item['snippet']['title'].encode('shift_jis', errors='ignore').decode('shift_jis'))
            print('動画ID:', item['id']['videoId'])
            id.append(item['id']['videoId'])
    return id


# 動画idから動画をダウンロード
def download(id_list):
    for id in id_list:
        print("Downloading {url} start..".format(url=id))
        with youtube_dl.YoutubeDL(download_options) as y:
            info = y.extract_info(id, download=True)
            print("Downloading {url} finish!".format(url=id))
        return info


if __name__ == "__main__":
    channel_list = search_channel_list()
    print(channel_list)
    id_list = search_movie(channel_list)
    print(id_list)
    info = download(id_list)
