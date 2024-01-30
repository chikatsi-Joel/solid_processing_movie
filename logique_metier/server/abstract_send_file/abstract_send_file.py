from abc import ABC, abstractmethod


class abstract_send_file(ABC) :

    @abstractmethod
    def set_new_path(self, path : str) :
        pass
    
    @classmethod
    def send_file(self) :
        pass

