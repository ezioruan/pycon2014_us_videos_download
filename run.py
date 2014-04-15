#-* coding:UTF-8 -*
#!/usr/bin/env python

import gevent.monkey
gevent.monkey.patch_all()
import os
import bs4
import requests
import gevent
import subprocess

here = os.path.abspath(os.path.dirname(__file__))
index_url = 'http://pyvideo.org/category/50/pycon-us-2014'
download_dir = os.path.join(here,"download")
if not os.path.exists(download_dir):
    print 'create dir',download_dir
    os.mkdir(download_dir)
api_url = "http://pyvideo.org/api/v2/video/%s?format=json"


def get_videos():
    resp = requests.get(index_url)
    print resp
    soup = bs4.BeautifulSoup(resp.text)
    video_div_list = soup.find_all('div',{'class':'video-summary-data'})
    print 'get %d video' % len(video_div_list)
    videos = [v.find_all('a')[0].attrs.get('href') for v in video_div_list]
    return videos

def _download_video(url,file_path):
    print 'begin to download %s , save to %s ' % ( url,file_path)
    download_cmd = 'youtube-dl %s -o %s' % (url,file_path)
    print download_cmd
    #subprocess.Popen(download_cmd)
    os.system(download_cmd)


def download_video():
    video_links = get_videos()
    downloads = []
    for link in video_links:
        video_id = link.split('/')[2]
        title = link.split('/')[-1] 
        video_info = requests.get(api_url%video_id).json()
        source_url = video_info['source_url']
        file_path = os.path.join(download_dir,"%s.mp4" % title)
        downloads.append(gevent.spawn(_download_video,source_url,file_path))
    gevent.joinall(downloads)






















if __name__ == "__main__":
    download_video()

