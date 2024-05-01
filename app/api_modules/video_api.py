from flask import Flask, request, Blueprint
from app import app
from app.modules import video
import base64


video_api = Blueprint('video_api', __name__)

@app.get('/test')
def video_test():
    return 'video works'

@app.route('/get_video', methods=['POST'])
def get_video():
    body = request.json
    video_name = body['video_name']
    print('video name', video_name)
    video_url = video.get_video_from_storage(video_name)
    return video_url

@app.route('/store_video', methods=['POST'])
def store_video():
    body = request.json
    file = rf'{body['file']}'
    vide_name = body['video_name']
    result = video.upload_video(file, vide_name)
    return result

@app.route('/store_info', methods=['POST'])
def store_info():
    body = request.json
    result = video.store_video_information(body)
    return result

@app.route('/get_videos_info', methods=['GET'])
def get_videos_info():
    result = video.load_videos_information()
    return result