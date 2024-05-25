import os, googletrans
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio


def vague(text : str) :
    number = len(text)//5000
    
    for i in range(1, number+1) :
        yield text[(i-1)*5000:i*5000]
    
    yield text[number*5000:]  
    
def epure(text:  str) :
    text =  text.replace(' -> ', ' --> ')
    text = text.replace('0->', ' -->')
    text = text.replace('：', ':')
    text = text.replace(': ', ':')
    text = text.replace(' 000', ',000')
    text = text.replace(' 00 ', ',000 ')
    return text


def translate_with_language(text : str, language_dest : str, language_src : str = 'auto') -> str | None :
    translate = googletrans.Translator().translate(text, dest = language_dest, src = language_src).text
    return translate


def extract_audio(video_path : str, audio_name : str, format : str) -> str | None:
    ffmpeg_extract_audio(video_path, "Audio/" + audio_name + "." +format)
    return "Audio/" + audio_name + "." +format
    
