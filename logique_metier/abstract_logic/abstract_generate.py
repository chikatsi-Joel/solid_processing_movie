
from abc import (ABC, abstractmethod)

class abstract_generate(ABC) :
    
    @abstractmethod
    def generate_file(file_path : str) : ...
