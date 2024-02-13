
from abc import (ABC, abstractmethod)

class abstract_generate(ABC) :
    
    @abstractmethod
    def generate_file(cls, file_path : str) -> str: ...
