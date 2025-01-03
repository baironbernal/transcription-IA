import pytest
import os
from io import BytesIO
from flask import Flask
from main import app  # assuming your Flask app is in 'app.py'

# Test for uploading audio
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test to upload an audio file and check transcription
def test_upload_audio(client):
    # Create a dummy audio file (for testing purposes)
    audio_data = BytesIO(b"dummy audio data")
    audio_data.seek(0)  # Reset pointer to the start of the file

    # Prepare the file to send
    data = {
        'file': (audio_data, 'test_audio.mp3')
    }

    # Simulate the POST request to upload the audio file
    response = client.post('/upload-audio', content_type='multipart/form-data', data=data)

    # Check if the response is a 200 OK and contains the transcription field
    assert response.status_code == 200
    response_json = response.get_json()
    
    # If the file is processed correctly, we expect a transcription field in the response
    assert 'transcription' in response_json

# Test when no file is provided
def test_upload_no_file(client):
    response = client.post('/upload-audio', data={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'No file part'

# Test when no file is selected
def test_upload_empty_file(client):
    data = {'file': (BytesIO(b"dummy"), '')}  # Empty file
    response = client.post('/upload-audio', content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'No selected file'

