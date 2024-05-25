from faster_whisper import WhisperModel
from datetime import timedelta
import random, string
from ..backbone import audio
from ..generate.convert_pdf import convertir



def get_name_gen(type_ : str) :
    lang = {
            'anglais' : 'en',
            'français' : 'fr',
            'russe' : 'ru',
            'protugais' : 'pt',
            'allemand' : 'de',
            'italien' : 'it',
            'japonais' : 'ja',
            'chinois' : 'zh'
    }
    return lang[type_]

def generate_name(number : int) :
    return ''.join([string.ascii_letters[random.randint(0, 10)]+str(random.randint(0, 5)) for _ in range(number)])

def transcribe_audio(audio_path : str, pdf_or_srt : str,  language_src : str, language_dest : str, type : str, horo_name : str, path_srt : str):
    model = WhisperModel("base")
    segments, info = model.transcribe(audio_path, beam_size = 5)

    texte = ""
    segmentId : int = 0
    for segment in segments:
        segmentId += 1
        startTime = str(0)+str(timedelta(seconds=int(segment.start)))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment.end)))+',000'
        text = segment.text
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        texte += segment

    generate = audio.vague(texte)
    url = f'{path_srt}/{horo_name}.srt'
    res = ""

    if language_dest != language_src :
        for portion in generate :
            trans = audio.translate_with_language(portion, language_dest = get_name_gen(language_dest.lower()), language_src = get_name_gen(language_src.lower()))
            res += trans
        with open(url, 'w', encoding='utf-8') as srtFile:
            srtFile.write(audio.epure(res))
    else :
        res = texte
        with open(url, 'w', encoding='utf-8') as srtFile:
            srtFile.write(texte)

    if pdf_or_srt == "PDF" :
        url_srt = url
        url_pdf = f'{path_srt}/{horo_name}.pdf'

        convertir.convert_srt_en_pdf(url_pdf, url_srt)
    
   
    return url

def traduct_srt(lang_src : str, lang_dest : str, srt_path : str = None, data_srt : str = None) :
    
    data = open(srt_path, "r").read()
    generate = audio.vague(data)
    res = ""
    for portion in generate :
        trans = audio.translate_with_language(portion, language_dest = get_name_gen(lang_dest), language_src = get_name_gen(lang_src))
        res += trans
    src_path = srt_path.split('/')[-1].split('.')[0]
    with open(f'Transcribe/{src_path}_{lang_dest}.srt', 'w', encoding='utf-8') as srtFile:
            srtFile.write(audio.epure(res))
    return srt_path

model = WhisperModel("base")

