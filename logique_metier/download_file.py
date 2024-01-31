
from logique_metier.abstract_logic.abstract_download import abstract_download

class download_file_logic(object) :
    
    @classmethod
    def download(cls, generator_utils : abstract_download) :
        return generator_utils.download_file()




