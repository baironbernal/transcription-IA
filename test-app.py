import pytest
from io import BytesIO
from flask import Flask
from main import app  # Assuming your Flask app is in 'main.py'
import warnings
import os

# Suppress FutureWarning related to torch.load
warnings.filterwarnings("ignore", category=FutureWarning, message=".*weights_only=False.*")

# Test for uploading audio
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test to upload an audio file and check transcription
def test_upload_audio(client):
    # Check if the audio file exists
    audio_file_path = 'audio/perro-come.mp4'
    if not os.path.exists(audio_file_path):
        pytest.fail(f"Test audio file {audio_file_path} does not exist")

    # Open the real audio file (audio/perro-come.mp4)
    with open(audio_file_path, 'rb') as audio_file:
        audio_data = BytesIO(audio_file.read())  # Read the file as a byte stream
        audio_data.seek(0)  # Reset pointer to the start of the file

    # Prepare the file to send
    data = {
        'file': (audio_data, 'perro-come.mp4')
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
