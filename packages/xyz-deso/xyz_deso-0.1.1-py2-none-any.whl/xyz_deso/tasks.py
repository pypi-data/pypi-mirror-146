# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task, chord
from . import helper

__author__ = 'denishuang'
import logging

log = logging.Logger("celery")


@shared_task(bind=True, time_limit=600)
def upload_video(self, path, **kwargs):
    helper.upload_video_post(path, '')