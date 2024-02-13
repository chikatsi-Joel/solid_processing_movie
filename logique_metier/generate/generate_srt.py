from ..abstract_logic import abstract_generate
from ..backbone import backbone_srt
from .convert_pdf import convertir

class generate_srt(abstract_generate) :
    @staticmethod
    def generate_file(file_path : str, text : str) :
        open(file_path, "r").write(text)
        return file_path
    

class generate_pdf(abstract_generate) :
    def __init__(self, pdf_path : str) :
        self.pdf_path = pdf_path
    @staticmethod
    def generate_file(file_path : str, texte : str) :
        generate_srt.generate_file(file_path, texte)
        convertir.convert_srt_en_pdf()


