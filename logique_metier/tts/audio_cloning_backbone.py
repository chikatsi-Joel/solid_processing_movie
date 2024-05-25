import torch
from TTS.api import TTS

device =  "cpu"


def tts_apply(text : str, speaker_audio : str, language : str,  file_path_output : str) :

    tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)
    tts.tts_to_file(text, speaker_wav=speaker_audio, language=language, file_path=file_path_output)