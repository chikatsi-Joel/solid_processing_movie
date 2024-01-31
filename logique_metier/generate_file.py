
from abstract_logic.abstract_generate import abstract_generate
from logique_metier.generate import generate_srt


class generate_file_logic(object) :
    def __init__(self ) :
        self.path : str

    def generate_file(self, generator_utils : abstract_generate | None = None) :
        generator_utils.generate_file(self.path)

