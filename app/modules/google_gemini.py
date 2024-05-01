import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from google.cloud import speech_v1p1beta1 as speech
from app.modules import video
import os
import time
import requests
import tempfile
import wave
from moviepy.editor import *
import subprocess

user = os.environ.get('USERNAME')
temp_dir = fr'C:\Users\{user}\AppData\Local\Temp'
#filename = r'C:\Users\Edgard Gamboa\AppData\Local\Temp\testAudio.mp3'
import base64

def is_linear16(filename):
    with wave.open(filename, 'rb') as wf:
        return wf.getsampwidth() == 2
        filename = "your_audio_file.wav"
        if is_linear16(filename):
            print("The audio is in linear16 format.")
        else: print("The audio is not in linear16 format.")

def audio_to_text(audio_media, temp_dir):
    #video.upload_audio(audio_media, audio_name)
    #audio_path = video.get_audio_from_storage(audio_name)
    print('audio_path', type(audio_media))
    #audio_content = base64.b64encode(audio_media)
    #time.sleep(60)
    output_file = rf'{temp_dir}\testAudioProccesed.wav'
    convert_webm_to_wav1(audio_media, output_file)
    with open(output_file, 'rb') as f:
        audio_content_temp = f.read()
        #audio_content = base64.b64encode(audio_content_temp)
        #audio_to_send = base64.b64decode(audio_content)
        #print('decode',audio_to_send)
        #print('encode',audio_content)
    client = speech.SpeechClient()

    #with open(audio_media, 'rb') as audio_file:
        #content = audio_file.read()
    #content = "https://storage.cloud.google.com/eggboa-audi/audio-files/segment_1.wav"

    audio = speech.RecognitionAudio(content=audio_content_temp)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code='es'
    )

    response = client.recognize(config=config, audio=audio)

    if os.path.exists(audio_media):
        os.remove(audio_media)
    elif os.path.exists(output_file):
        os.remove(output_file)

    # Extract transcriptions from response
    transcriptions = [result.alternatives[0].transcript for result in response.results]
    print(transcriptions)

    result = ' '.join(transcriptions)
    print("result----", result)
    return {'success':True,
            'text': result}

def generate(audio):
    client = speech.SpeechClient()

    with open(audio, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding='mp3',
        language_code='en-US'

    )

    response = client.recognize(config=config, audio=audio)

    # Extract transcriptions from response
    transcriptions = [result.alternatives[0].transcript for result in response.results]

    result = ' '.join(transcriptions)
    return result

def multiturn_generate_content(sentence_to, interpretation):
  vertexai.init(project="gen-lang-client-0267084365", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-pro-preview-0409",
  )
  model_response = model.generate_content(["Please judge the following language translation and output either pass"
                                           " or fail. if its 70% correct then pass it. Not every word needs to be "
                                           "correct. Only output pass or fail and feedback. no explanation.",
                                           sentence_to, interpretation], stream=False)

  return model_response.candidates[0].content.parts[0].text
  ##chat = model.start_chat()


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.7,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

#multiturn_generate_content( "It looks like you just"
                                           # "got an Xray", "parece que ah hecho una radiografía ")

def convert_webm_to_wav(input_file, output_file):
    # Load the WebM video file
    video = VideoFileClip(input_file)

    # Extract audio
    audio = video.audio

    # Write audio to WAV file
    audio.write_audiofile(output_file, codec='pcm_s16le')  # Save as WAV

def convert_webm_to_wav1(input_file, output_file):
    command = [
        'ffmpeg',
        '-y',
        '-i', input_file,  # Input file (WebM)
        '-vn',             # Suppress video
        '-acodec', 'pcm_s16le',  # Set audio codec to PCM 16-bit signed little-endian
        '-ar', '44100',    # Set audio sample rate to 44100 Hz
        '-ac', '1',        # Set audio channels to stereo
        output_file        # Output file (WAV)
    ]
    subprocess.run(command, check=True)
# Provide input and output file paths
output_file = r'C:\Users\Edgard Gamboa\AppData\Local\Temp\testAudioProccesed.wav'
input_file = r'C:\Users\Edgard Gamboa\AppData\Local\Temp\testAudio.wav'

#is_linear16(r'C:\Users\Edgard Gamboa\AppData\Local\Temp\testAudio.wav')
#file_path = r'C:\Users\Edgard Gamboa\Downloads\Recording.wav'
#convert_webm_to_wav(file_path, output_file)
#print("Audio extracted and saved as WAV:", output_file)
#convert_webm_to_wav1(input_file, output_file)
#audio_format = detect_audio_format(output_file)
#print("Audio file format:", audio_format)
#audio_to_text(output_file)