
from abc import (ABC, abstractmethod)

class abstract_download(ABC) :
    
    @abstractmethod
    def download_file() -> str: 
        raise Exception("is abstract method")