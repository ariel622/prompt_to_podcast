import pyttsx3
import os
import json
import http.client
from gtts import gTTS

# Load configuration
def load_config():
    with open('configurations\config.json', 'r') as f:
        return json.load(f)

# Function to convert text to speech and save as a file
def convert_and_save_text_to_speech(text, base_filename="new_episode.mp3", rate=150, voice_index=0):
    engine = pyttsx3.init()
    
    # Set speech rate
    engine.setProperty('rate', rate)

    # List available voices and select one
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Index: {index} - Voice: {voice.name}, Lang: {voice.languages}, Gender: {voice.gender}, ID: {voice.id}")

    if voice_index >= len(voices):
        print("Warning: Requested voice index is out of range. Defaulting to first voice.")
        voice_index = 0  # Default to the first voice if out of range

    engine.setProperty('voice', voices[voice_index].id)  # Set voice by index

    # Filename handling
    filename = base_filename
    counter = 1
    while os.path.exists(filename):
        parts = base_filename.split('.')
        parts[0] += f"_{counter}"
        filename = '.'.join(parts)
        counter += 1

    # Save to file and process speech
    engine.save_to_file(text, filename)
    engine.runAndWait()  # Processes the speech synthesis request
    print(f"Saved new episode as: {filename}")

def tts_maker_api(text, lang='en', voice='default'):
    config = load_config()
    conn = http.client.HTTPSConnection("api.ttsmaker.com")  # Adjust API URL accordingly
    payload = json.dumps({
        "text": text,
        "lang": lang,
        "voice": voice
    })
    headers = {
        'Authorization': 'Bearer ' + config['api_key'],  # Make sure your config includes the API key
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/speech", payload, headers)  # Adjust API path accordingly
    res = conn.getresponse()
    audio_data = res.read()  # Adjust based on whether you receive a URL or actual audio data
    return audio_data

# Function to save the podcast with a unique name
def save_podcast(audio_data, base_filename="new_episode.mp3"):
    filename = base_filename
    counter = 1
    while os.path.exists(filename):
        parts = base_filename.split('.')
        parts[0] += f"_{counter}"
        filename = '.'.join(parts)
        counter += 1
    audio_data.save(filename)
    print(f"Saved new episode as: {filename}")

def generate_prompt_from_subject(subject):
    return (
        f"אתה כותב תסריט לפודקאסט שנדרש ליצור תוכן מרתק ונצחי בנושא {subject}. "
        "אנא צור תסריט מפורט ומועיל המתאים לפרק באורך של כ-15 דקות, עם דגש על נושאים כלליים ואי-זמניים. "
        "התסריט צריך להיות נטול התייחסויות לתפקידים כגון מנחה או אורח, וללא הוראות עריכה או מוזיקת פתיחה."
    )

# Function to generate podcast script using OpenAI API
def generate_podcast_script(prompt):
    config = load_config()
    conn = http.client.HTTPSConnection(config["api_url"])
    payload = json.dumps({
        "model": "gpt-3.5-turbo-16k-0613",
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 1.0,  # Optional: Adjusts the probability distribution during sampling to control creativity
        "messages": [
            {
                "role": "assistant",
                "content": "אתה כותב תסריט לפודקאסט שנדרש ליצור תוכן מרתק ונצחי בנושא {subject}. אנא צור תסריט מפורט ומועיל המתאים לפרק באורך של כ-15 דקות, עם דגש על נושאים כלליים ואי-זמניים."
    

                #"content": "You are a bot that gets a subject and returns a full detailed and informative podcast transcript. Make it long (15 minutes)"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    conn.request("POST", config["api_path"], payload, config["headers"])
    res = conn.getresponse()
    data = res.read()
    return json.loads(data)["choices"][0]["message"]["content"]




# OLD def generate_podcast_script(subject):
#     config = load_config()
#     conn = http.client.HTTPSConnection(config["api_url"])
#     payload = json.dumps({
#         "model": "gpt-3.5-turbo-1106",
#         "messages": [
#             {
#                 "role": "assistant",
#                 "content": "You are a bot that generates engaging and timeless content for a podcast episode. Please produce a detailed and informative script about a broad and evergreen topic. The episode should last about 15 minutes."

#                 #"content": "You are a bot that gets a subject and returns a full detailed and informative podcast transcript. Make it long (15 minutes)"
#             },
#             {
#                 "role": "user",
#                 "content": subject
#             }
#         ]
#     })
#     conn.request("POST", config["api_path"], payload, config["headers"])
#     res = conn.getresponse()
#     data = res.read()
#     return json.loads(data)["choices"][0]["message"]["content"]

# Main function to handle workflow

def main():
    subject = input("Enter Subject: ")
    prompt = generate_prompt_from_subject(subject)
    script = generate_podcast_script(prompt)
    print(str(script) + "\n")

    tts = gTTS(text=script, lang='iw')
    save_podcast(tts)
    # audio_data = tts_maker_api(script, 'en')
    # save_podcast(audio_data)
    # convert_and_save_text_to_speech(script, rate=120, voice_index=1)  # Adjust rate and voice index as needed

    print("Ready!")

if __name__ == "__main__":
    main()
