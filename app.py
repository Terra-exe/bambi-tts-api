from flask import Flask, request, jsonify
import threading
import os
import sys
import re
import json
import boto3
from botocore.exceptions import NoCredentialsError


sys.path.insert(3, r'\\SERVER\Magnum Opus\dump\audio')

from . import kriya_object

polly = boto3.client('polly')
s3 = boto3.client(
        's3',
        region_name='us-west-2',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

def synthesize_speech(text, output_format='mp3', voice_id='Salli'):
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id
    )
    return response['AudioStream'].read()

def upload_to_s3(bucket_name, audio_data, s3_key):
    
    try:
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=audio_data, ContentType='audio/mpeg')
        return f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
    except NoCredentialsError:
        print("No AWS credentials provided")
        return None

def json_to_audio(jsondata, bucket_name):
    kriya_obj = kriya_object.create_kriya_obj_from_json(jsondata)
    filename = kriya_obj.title.replace(".json", "")

    # Generate the audio using Amazon Polly
    audio_data = synthesize_speech(filename)

    # Upload the generated audio to Amazon S3
    s3_key = f"{filename}.mp3"
    audio_url = upload_to_s3(bucket_name, audio_data, s3_key)

    return audio_url

# Initialize Flask app
app = Flask(__name__)

@app.route('/bambi-tts-api', methods=['POST'])
def handle_tts_request():
    jsondata = {}
    print("POST received")
    try:
        jsondata = request.get_json()  # get the JSON object from the request
        print("Received data: ", jsondata)

        audio_url = json_to_audio(jsondata, 'your-s3-bucket-name')

        if audio_url:
            return jsonify({'message': 'Audio file created successfully', 'audio_url': audio_url}), 200
        else:
            return jsonify({'message': 'Error occurred while creating audio file'}), 500

    except Exception as e:
        print("Error: ", str(e))
        return {"success": False},

if __name__ == "__main__":
    app.run()