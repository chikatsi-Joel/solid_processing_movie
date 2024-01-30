from abc import ABC, abstractmethod



class abstract_bd_musical(object) :
    
    def __init__(
        self,
        name : str, 
        categorie : str,
        description : str
    ) :
        self.name = name
        self.categorie = categorie
        self.description = description

    @abstractmethod
    def get_movie_by_class_and_categorie(self, name : str, categorie : str) -> dict[str, str ]: ...
