#!/usr/bin/python3

from google.cloud import storage
import time, os, sys
import base64
import subprocess
import pyrebase
import logging
import json

config = json.loads(open('database.json', 'r').read())

firebase = pyrebase.initialize_app(config)


def database(timestamp, vurl, purl, vlength):
    db = firebase.database()
    data = {
        "timestamp": timestamp,
        "video_url": vurl,
        "picture_url": purl,
        "duration": vlength
    }
    db.push(data)


def upload(filename, timestamp, filetype):
    client = storage.Client.from_service_account_json(json_credentials_path='cloud-storage.json')
    bucket = client.get_bucket('trail-cam-footage')

    file = bucket.blob(base64.b64encode(timestamp.encode("ascii")).decode('ascii') + filetype)
    file.upload_from_filename(filename)
    file.make_public()
    return file.public_url

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=nologging.info_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


logging.basicConfig(filename="main.log", level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logging.info('New event finished, motion logging begining.')

if len(sys.argv) == 3:
    media = sys.argv[1]
    event_time = sys.argv[2]
    if media.lower().endswith('.mp4'):
        vid_length = get_length(media)
        logging.info('Motion lasting {} seconds completed. Begining uploading...'.format(vid_length))
        vid_url = upload(media, event_time, '.mp4')
        logging.info('Video saved to {}'.format(vid_url))
        f = open("/home/pi/TrailCam/motion/video.txt", "w")
        f.write("{} & {}".format(vid_length, vid_url))
        f.close()
    elif media.lower().endswith('.jpg'):
        pic_url = upload(media, event_time, '.jpg')
        logging.info('Picture saved to {}'.format(pic_url))
        f = open("/home/pi/TrailCam/motion/video.txt", "r")
        vid_url, vid_length = f.read().split(" & ")
        database(event_time, vid_url, pic_url, vid_length)
        logging.info('Log database entries updated. Deleting local files...')
    os.remove(media)
    logging.info('Local files deleted. Waiting for new motion event...')
else:
    logging.info(sys.argv)