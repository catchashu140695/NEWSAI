import warnings
from pydub import AudioSegment
import whisper
import yt_dlp as youtube_dl
import os
import logging
import json
from g4f.client import Client
import re
import asyncio
import speech_recognition as sr
import datetime




# Set the event loop policy for Windows
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def get_chat_response(prompt):
    try:
    # Initialize the client
        client = Client()
        
        # Create a chat completion request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        print("")
        print("GPT Response:")
        print(response.choices[0].message.content)
        # Return the response content
        return response.choices[0].message.content  # Access content attribute directly

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def format_timedelta(td):
    """Format a timedelta to the SRT format: hh:mm:ss,ms"""
    total_seconds = int(td.total_seconds())
    milliseconds = int(td.microseconds / 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def transcribe_and_save_srt(audio_path, output_dir, lang='hi-IN', chunk_length_ms=5000):
    """
    Transcribe Hindi audio and save the transcription in SRT format with timestamps.
    
    Parameters:
        audio_path (str): Path to the audio file.
        output_dir (str): Directory to save the SRT file.
        lang (str): Language code for transcription (default is Hindi).
        chunk_length_ms (int): Length of audio chunks in milliseconds (default is 60 seconds).
    """
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)
    
    # Create chunks of audio
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    
    transcript = []
    current_time = datetime.timedelta()

    for i, chunk in enumerate(chunks):
        chunk_path = f'temp_chunk_{i}.wav'
        chunk.export(chunk_path, format='wav')
        
        with sr.AudioFile(chunk_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language=lang)
                transcript.append((current_time, current_time + datetime.timedelta(seconds=chunk.duration_seconds), text))
            except sr.UnknownValueError:
                transcript.append((current_time, current_time + datetime.timedelta(seconds=chunk.duration_seconds), "[Unintelligible]"))
            except sr.RequestError:
                transcript.append((current_time, current_time + datetime.timedelta(seconds=chunk.duration_seconds), "[Error]"))

        # Update current time
        current_time += datetime.timedelta(seconds=chunk.duration_seconds)
        os.remove(chunk_path)

    # Save to SRT file
    output_path = os.path.join(output_dir, 'transcript.srt')
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, (start, end, line) in enumerate(transcript):
            f.write(f"{i}\n")
            f.write(f"{format_timedelta(start)} --> {format_timedelta(end)}\n")
            f.write(f"{line}\n\n")
    
    print(f"Transcript saved to {output_path}")

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_video_with_audio(url, path=None):
    if path is None:
        path = os.path.expanduser('./AI-video-maker/final work/raw_video')
    
    ensure_directory_exists(path)

    ydl_opts = {
        'outtmpl': f'{path}/video.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Downloaded video from {url} to {path}")
            return os.path.join(path, 'video.mp4')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_audio_from_video(video_path, output_path=None):
    if output_path is None:
        output_path = os.path.dirname(video_path)
    
    ensure_directory_exists(output_path)

    try:
        # Load the video clip
        video_clip = AudioSegment.from_file(video_path, format="mp4")

        # Export audio
        audio_file_path = os.path.join(output_path, 'audio.mp3')
        video_clip.export(audio_file_path, format="mp3")

        return audio_file_path

    except Exception as e:
        print(f"Error: {e}")
        return None


def parse_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove time frames and numbers
    content = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', content)
    # Remove "[Unintelligible]"
    content = content.replace('[Unintelligible]', '')
    # Remove empty lines and concatenate
    result = ' '.join(content.splitlines()).strip()
    
    return result


def extract_between_brackets(s):
    start = s.find('[') + 1
    end = s.rfind(']')
    if start > 0 and end > start:
        return s[start:end]
    else:
        return "No valid substring found"

def analyze_transcript(subtitle_file_path):
    print("Analyze transcript begins")
    
    # Read content from subtitle file
    subtitle_content = parse_srt(subtitle_file_path)

    # Define the expected JSON format
    response_obj = [
        {
            "start_time": "0.0",
            "end_time": "55.26",
            "description": "main description",
            "duration": "55.26"
        },
        {
            "start_time": "57.0",
            "end_time": "107.96",
            "description": "second main description",
            "duration": "50.96"
        }
        
    ]

    # Process the entire content as one prompt
    prompt='From the summary choose a viral part. Summary:' + subtitle_content
    print("")
    print("Prompt:")
    print(prompt)
    
    combined_response = extract_between_brackets(get_chat_response(prompt))    
        
    # Logging the combined response for debugging
    logging.info(f"Combined Response: {combined_response}")

    # Validate if the response is non-empty and valid JSON
    if not combined_response:
        logging.error("The response is empty")
        return

    try:
        response_json = json.loads(combined_response)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        return

    with open('main_part.json', 'w') as json_file:
        json.dump({"combined_response": response_json}, json_file, indent=2)  # Use indent to format the JSON nicely

    return response_json




if __name__ == "__main__":
    #Replace 'your_video_url' with the actual URL of the YouTube video
    # video_url = 'https://www.youtube.com/watch?v=crH7kpjomIk'

    # # Download the video with audio into the specified output path with the file name "video_with_audio.mp4"
    # video_with_audio_path = download_video_with_audio(video_url)

    # if video_with_audio_path:
    #     print(f"Video with audio saved at: {video_with_audio_path}")

    #     # Extract audio from the video
    #     extracted_audio_path = extract_audio_from_video(video_with_audio_path)

    #     if extracted_audio_path:
    #         print(f"Extracted audio saved at: {extracted_audio_path}")

    #         audio_path = extracted_audio_path 
    #         output_dir = 'AI-video-maker/final work/raw_video' 
            
    #         if not os.path.exists(output_dir):
    #             os.makedirs(output_dir)
            
    #         transcribe_and_save_srt(audio_path, output_dir)
    #         # Extract subtitles from the audio
            
            
            
    #         # Delete the audio file after subtitle extraction
    #         #os.remove(extracted_audio_path)
    #         #print("Audio file deletszzzzzzzzzzed.")
        # Example usage
        subtitle_path = r"AI-video-maker\final work\raw_video\transcript.srt"  # Use raw string literal
        analyze_transcript(subtitle_path)       
            
            
            
