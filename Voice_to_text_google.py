import speech_recognition as sr
from pydub import AudioSegment # Used for conversion
import os

# --- Part 1: Convert .ogg to .wav ---
# ogg_file = os.path.join("voice_downloads", "voice_324441.ogg")
wav_file = "converted_message.wav"
def Convert(Download_path):

    try:
        # Load the .ogg file
        audio = AudioSegment.from_ogg(Download_path)        
        # Export it as a .wav file
        audio.export(wav_file, format="wav")

    except Exception as e:
        print(f"Could not convert file. Make sure FFmpeg is installed and in your system's PATH.")
        print(f"Error: {e}")
        exit() # Exit if conversion fails

    r = sr.Recognizer()

    # Open the .wav file
    with sr.AudioFile(wav_file) as source:
        # Read the audio data
        audio_data = r.record(source)
        
        # Try to recognize the speech using Google's free web API
        try:
            text = r.recognize_google(audio_data, language="fa-IR")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google; {e}")
    if os.path.exists(wav_file):
            os.remove(wav_file)

    if os.path.exists(Download_path):
        os.remove(Download_path)   
        
    return text
