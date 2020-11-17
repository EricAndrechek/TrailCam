from google.cloud import storage
import time, os
import base64
import subprocess
import pyrebase
import logging
import json

config = json.loads(open('database.json', 'r').read())

firebase = pyrebase.initialize_app(config)
logging.basicConfig(filename="main.log", level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

def log_reader():
    logging.info('Pi has booted. Motion logging begining.')
    file = open('motion.log','r')

    st_results = os.stat('motion.log')
    st_size = st_results[6]
    file.seek(st_size)
    last_vid = ""
    pic_path = ""
    event_time = ""

    while 1:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            if "File of type 1 saved to:" in line:
                pic_path = line.split("File of type 1 saved to: ")[1].rstrip()
            elif "File of type 8 saved to:" in line:
                last_vid = line.split("File of type 8 saved to: ")[1].rstrip()
            elif "End of event" in line:
                vid_length = get_length(last_vid)
                logging.info('Motion lasting {} seconds completed. Begining uploading...'.format(vid_length))
                vid_url = upload(last_vid, event_time, '.mp4')
                logging.info('Video saved to {}'.format(vid_url))
                pic_url = upload(pic_path, event_time, '.jpg')
                logging.info('Picture saved to {}'.format(pic_url))
                database(event_time, vid_url, pic_url, vid_length)
                logging.info('Log database entries updated. Deleting local files...')
                os.remove(last_vid)
                os.remove(pic_path)
                logging.info('Local files deleted. Wait for new motion event...')
            elif "Motion detected - starting event" in line:
                event_time = line.split("] motion_detected: Motion detected - starting event")[0].split("[ALL] [")[1]
                logging.info('\nMotion detected at {}'.format(event_time))

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

log_reader()