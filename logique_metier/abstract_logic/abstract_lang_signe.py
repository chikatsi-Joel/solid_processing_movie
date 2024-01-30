from abc import ABC, abstractmethod



class abstract_lang_signe(object) :

    @abstractmethod
    def get_text_to_video(self) -> str: ...

    @abstractmethod
    def get_dimension_to_text(self) -> str : ...

    @abstractmethod
    def get_(self) -> str : ...