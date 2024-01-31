
from abc import (ABC, abstractmethod)

class abstract_download(ABC) :
    
    @abstractmethod
    def download_file() -> str: 
        raise NotImplementedError("is abstract method")