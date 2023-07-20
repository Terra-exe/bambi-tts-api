from flask import Flask, request, jsonify
import threading
import os
import sys
import re
import json
import boto3
import logging
from botocore.exceptions import NoCredentialsError
import json_builder.bin.kriya_object as kriya_object
"""
polly = boto3.client(
    'polly',
    region_name='us-west-2',
)

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

def upload_to_s3(bucket_name, s3_key, audio_data):
    try:
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=audio_data, ContentType='audio/mpeg')
        return True
    except NoCredentialsError:
        print("No AWS credentials provided")
        return False

def create_hello_world_audio():
    logging.debug("Creating 'Hello World' audio")
    bucket_name = 'crystal-audio-processing'
    s3_key = 'audio-dumps/audio-gen-files/hello_world.wav'
    audio_data = synthesize_speech("Hello World")
    success = upload_to_s3(bucket_name, s3_key, audio_data)
    if success:
        logging.debug("Successfully uploaded 'Hello World' audio to S3")
    else:
        logging.debug("Failed to upload 'Hello World' audio to S3")
    return success

def json_to_audio(jsondata, bucket_name, s3_key):
    kriya_obj = kriya_object.create_kriya_obj_from_json(jsondata)
    filename = kriya_obj.title.replace(".json", "")
    audio_data = synthesize_speech(filename)
    success = upload_to_s3(bucket_name, s3_key, audio_data)
    return success


"""



app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
 """
@app.route('/bambi-tts-api', methods=['POST'])
def handle_tts_request():
    logging.debug("Received POST request")
    jsondata = {}
    print("POST received")
    try:
        jsondata = request.get_json()
        print("Received data: ", jsondata)
        bucket_name = 'crystal-audio-processing'
        s3_key = 'audio-dumps/audio-gen-files/crystal_demo.wav'
        success = json_to_audio(jsondata, bucket_name, s3_key)
        if success:
            return jsonify({'message': 'Audio file created successfully'}), 200
        else:
            return jsonify({'message': 'Error occurred while creating audio file'}), 500
    except Exception as e:
        print("Error: ", str(e))
        return {"success": False},
"""
if __name__ == "__main__":
    print("Running App")
    #create_hello_world_audio()
    app.run()