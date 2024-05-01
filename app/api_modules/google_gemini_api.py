from flask import Flask, request, Blueprint
from app import app
from app.modules import google_gemini
import os
import tempfile
app.config['MAX_CONTENT_LENGTH'] = 80 * 1024 * 1024

gemini_api = Blueprint('gemini_api', __name__)
user = os.environ.get('USERNAME')
#temp_dir = fr'C:\Users\{user}\AppData\Local\Temp'
import base64
temp_dir = tempfile.mkdtemp()
print('tempPath', temp_dir)

@app.get('/')
def boom():
    return 'hello world'

@app.route('/interpret', methods=['POST'])
def interpret():
    body = request.json
    interpretation = body['interpretation']
    sentence_to = body['sentence_to']
    score = google_gemini.multiturn_generate_content(sentence_to, interpretation)
    print(score)
    return {"score":score}

@app.route('/audio_to_text', methods=['POST'])
def audio_to_text():

    #request.files['audio'].save(r'C:\Users\Edgard Gamboa\documents')
    audio_file = request.files.get('audio')
    audio_file_path = rf'{temp_dir}\testAudio.wav'


    audio_file.save(audio_file_path)
    #data = base64

    #print(audio_file.name)
    text = google_gemini.audio_to_text(audio_file_path, temp_dir)
    return text
