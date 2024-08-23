import PyPDF2
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
load_dotenv()
# Initializing Eleven Labs
client = ElevenLabs(api_key=os.getenv("E_API"))
text = PyPDF2.PdfReader('./three.pdf')
starting = int(input("What page should I start reading from ? (e.g First page is zero, and Give an INT) "))
ending = input("What page should I end reading? (e.g, if to the last page type LAST, or type an int that > starting.)")
str_text = ""


# This is the function to remove unwanted or sentences
def filter_unwanted_text(text_need_cleaned, sentence=None):
    # Remove specific phrases or patterns
    # This is a simple example; you can use more complex regex if needed
    result = text_need_cleaned.replace(sentence, "")
    # You can also add more patterns to remove as needed
    return result.strip()


if ending == "LAST":
    page = len(text.pages)
else:
    page = int(ending)

while starting < int(ending):
    string = text.pages[starting].extract_text()
    string = filter_unwanted_text(string)
    str_text += string
    starting = starting+1

# This is where the text get played
audio = client.generate(
    text=str_text,
    voice="Rachel"
)
play(audio)
save(audio, "my-file.mp3")
