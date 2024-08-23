import PyPDF2
import requests
import base64
import os
from dotenv import load_dotenv
load_dotenv()

text = PyPDF2.PdfReader('./three.pdf')
starting = int(input("What page should I start reading from ? "))
str_text=""
def filter_unwanted_text(text):
    # Remove specific phrases or patterns
    # This is a simple example; you can use more complex regex if needed
    text = text.replace("Contents - Prev / Next", "")
    text = text.replace("Contents - Prev", "")
    # You can also add more patterns to remove as needed
    return text.strip()

while starting < len(text.pages):
    string=text.pages[starting].extract_text()
    str_text += string
    starting = starting+1

API_BASE_URL = "https://api.sws.speechify.com"
VOICE_ID = "george"
header = {
    "Authorization":'BEARER yx0eX1ozCyT0fdyl-w_tHAVl_A35Ykyo-A37EmEZ-Tc=',
    "Content-Type":"application/json"
}
ssml=f"<speak>{str_text}</speak>"
payload = {
    "input": ssml,
    "voice_id": VOICE_ID,
    "audio_format": "mp3"
}

response = requests.post(url=f"{API_BASE_URL}/v1/audio/speech", json=payload,headers=header)
response.raise_for_status()
response = response.json()
decoded_audio_data = base64.b64decode(response['audio_data'])
with open('output.mp3', 'wb') as audio_file:
    audio_file.write(decoded_audio_data)
