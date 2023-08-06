# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from deso.Post import Post as OPost
from deso.Post import getRoute, addExtraData, Sign_Transaction
import requests
from six import text_type

class Post(OPost):

    def send(self, content, imageUrl=[], videoUrl=[], postExtraData={}):
        # if user passed url for a single image as string, convert str into list[str]
        if isinstance(imageUrl, text_type):
            imageUrl = [imageUrl]
        if isinstance(videoUrl, text_type):
            videoUrl = [videoUrl]
        header = {
            "content-type": "application/json"
        }

        payload = {"UpdaterPublicKeyBase58Check": self.PUBLIC_KEY,
                   "PostHashHexToModify": "",
                   "ParentStakeID": "",
                   "Title": "",
                   "BodyObj": {"Body": content, "ImageURLs": imageUrl, "VideoURLs": videoUrl},
                   "RecloutedPostHashHex": "",
                   "PostExtraData": postExtraData,
                   "Sub": "",
                   "IsHidden":  False,
                   "MinFeeRateNanosPerKB": self.MIN_FEE
                   }
        ROUTE = getRoute()
        endpointURL = ROUTE + "submit-post"
        res = requests.post(endpointURL, json=payload, headers=header)
        transactionHex = res.json()["TransactionHex"]

        if self.DERIVED_KEY:
            transactionHex = addExtraData(transactionHex, self.DERIVED_KEY)

        signedTransactionHex = Sign_Transaction(
            self.SEED_HEX, transactionHex
        )  # txn signature

        submitPayload = {"TransactionHex": signedTransactionHex}
        endpointURL = ROUTE + "submit-transaction"
        submitResponse = requests.post(endpointURL, json=submitPayload)
        if submitResponse.status_code == 200:
            return {"status": submitResponse.status_code, "postHashHex": submitResponse.json()["TxnHashHex"]}
        else:
            return submitResponse.json()

    def uploadVideo(self, video):
        if isinstance(video, text_type):
            video = open(video, 'rb')
        ROUTE = getRoute()
        endpointURL = ROUTE + "upload-video"
        from .tus import upload
        r = upload(video, endpointURL)
        return 'https://iframe.videodelivery.net/%s' % r.headers['stream-media-id']
