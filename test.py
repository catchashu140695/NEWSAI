from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence

def save_news_audio():   
    database = "toshai.db"
    audio_directory = "./examples/driven_audio/"
    language = 'hi'
    tld = 'com'
    html = '''
    एक छोटे से गांव में एक बच्चा नामकरण के दिन के लिए तैयार हो रहा था। उसके माता-पिता ने उसे एक खास उपहार दिया - एक पुरानी किताब। वह किताब बच्चे के लिए अनमोल थी, क्योंकि उसमें जादू, राजकुमार, और खोज की कहानियाँ थीं।

    बच्चा नामकरण के दिन, उसने वह किताब खोली और एक कहानी पढ़ने लगा। वह कहानी एक जादूगर की थी, जो एक छोटे से गांव में रहता था। उसके पास एक जादूवी छड़ी थी, जिससे वह लोगों की मदद करता था।

    एक दिन, गांव में अचानक अच्छानक बारिश होने लगी। लोग घरों में जा रहे थे, लेकिन एक बुजुर्ग औरत अपने घर से निकली नहीं थी। वह बहुत बीमार थी और उसकी जरूरत थी।

    जादूगर ने अपनी छड़ी उठाई और बारिश को रोक दिया। वह बुजुर्ग औरत के घर पहुँचा और उसकी देखभाल की। उसकी सेवा करने से वह खुश हुआ और जादूगर की छड़ी को धन्यवाद दिया।

    इस कहानी से बच्चा समझ गया कि जादूगर की असली शक्ति उसकी सेवा करने में है। वह नामकरण के दिन अपने नाम के साथ एक नई शपथ ली कि वह भी लोगों की मदद करेगा।
    '''

    # Ensure the directory exists
    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    tts = gTTS(text=html, lang=language, slow=False)  
    temp_path = os.path.join(audio_directory, "temp.wav")
    tts.save(temp_path)

    # Load the generated speech
    audio = AudioSegment.from_file(temp_path)
    
    # Increase the playback speed
    speed = 1.25  # Speed factor (1.5 means 50% faster)
    faster_audio = audio.speedup(playback_speed=speed)
    
    # Trim silence at the end of sentences
    chunks = split_on_silence(faster_audio, min_silence_len=200, silence_thresh=-40)
    trimmed_audio = AudioSegment.empty()
    for chunk in chunks:
        trimmed_audio += chunk + AudioSegment.silent(duration=50)  # Add short silence between chunks

    # Save the trimmed and faster audio
    final_path = os.path.join(audio_directory, "file.wav")
    trimmed_audio.export(final_path, format="wav")

    # Remove the temporary file
    os.remove(temp_path)
    
    print(f"Audio file saved as {final_path}")

save_news_audio()
