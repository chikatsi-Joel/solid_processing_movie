from ..abstract_logic import abstract_generate
from ..backbone import backbone_srt

class generate_srt(abstract_generate) :
    def __init__(
        self, 
        file_path : str,
        horo_name : str,
        lang_dep : str,
        lang_src : str,
        type : str,
    ) :
        
        self.video_path = file_path
        self.horo_name = horo_name
        self.lang_dep = lang_dep
        self.lang_src = lang_src
        self.type = type

    def generate_file(file_path : str) :
        return backbone_srt.transcribe_audio(
            generate_srt.__dict__
        )
    

class generate_pdf(abstract_generate) :
    def __init__(
        self,
        file_path : str,
        format : str,
        lang_dep : str,
        lang_src : str,
        type : str
    ) :

        self.file_path = file_path
        self.format = format
        self.lang_dep = lang_dep
        self.lang_src = lang_src
        self.type = type

    def generate_file(file_path : str) :
        print(generate_pdf.__dict__)


