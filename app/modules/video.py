# Imports the Google Cloud client library
from google.cloud import storage
from io import BytesIO
import base64
from app.modules import DB
import os

# Instantiates a client
storage_client = storage.Client()

# The name for the new bucket
bucket_name = "eggboa-audi"

user = os.environ.get('USERNAME')
temp_dir = fr'C:\Users\{user}\AppData\Local\Temp'

def get_video_from_storage(video_name):
# Creates the new bucket
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(video_name)
    result = ""
    if blob == None:
        result = 'This video is having issues. Please try another video. '
    else:
        formattedName = blob.name.replace(" ", "%20")
        result = f'https://storage.cloud.google.com/{bucket_name}/{formattedName}'

    return {'videoURL':result}

def get_audio_from_storage(audio_name):
# Creates the new bucket

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob("audio-files/" + "testAudio.mp3")
    audio_path = rf'{temp_dir}\{audio_name}'
    blob.download_to_filename(audio_path)
    #blob.delete()

    return audio_path

def upload_video(file, video_name):
# Creates the new bucket
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(video_name)

        generation_match_precondition = 0

        upload = blob.upload_from_filename(rf'{file}', if_generation_match=generation_match_precondition)
        print(upload)
        return {'success':True}  # Upload successful
    except Exception as e:
        print(f"Error uploading file: {e}")
        return {'success':False,
                'error': str(e)}  # Upload failed

def upload_audio(file, audio_name):
# Creates the new bucket
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('audio-files/' + audio_name)

        generation_match_precondition = 0

        upload = blob.upload_from_filename(rf'{file}')
        print({'success':True})
        return {'success':True}  # Upload successful
    except Exception as e:
        print(f"Error uploading file: {e}")
        return {'success':False,
                'error': str(e)}  # Upload failed

def store_video_information(information):
    try:
        document_ref = information['video_name']
        data = DB.collection.add(information, document_id=document_ref)
        return {'success': True}  # Upload successful
    except Exception as e:
        print(f"Error uploading file: {e}")
        return {'success': False,
            'error': str(e)}  # Upload failed

def load_videos_information():
    videos_information_list = []
    try:
        data = DB.collection.stream()
        for doc in data:
            videos_information_list.append(doc.to_dict())
        print(videos_information_list)
        return videos_information_list  # Upload successful
    except Exception as e:
        print(f"Error uploading file: {e}")
        return {'success': False,
            'error': str(e)}  # Upload failed


#get_audio_from_storage("segment_1.wav")
#load_videos_information()
#upload_audio(r'C:\Users\Edgard Gamboa\Downloads\Recording.wav', 'RecordingTest')
#get_video_from_storage()