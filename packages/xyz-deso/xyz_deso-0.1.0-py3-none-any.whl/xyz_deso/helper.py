# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.conf import settings
from .Post import Post

CONF = settings.get('DESO', {})


def new_post():
    return Post(CONF['SEEDHEX'], CONF['PUBLIC_KEY'])


def upload_video_post(video_path, content=''):
    post = new_post()

    file_obj = open(video_path, "rb")

    url = post.uploadVideo(file_obj)
    post.send(content, videoUrl=[url])
