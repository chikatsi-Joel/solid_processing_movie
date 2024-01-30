import random

class color :
    colors = [(42, 134, 252 ), (179, 42, 252 ), (252, 102, 42 ), (42, 105, 252 ), (164, 124, 239 ), (124, 239, 124 )]

    @classmethod
    def get_color(cls, nbre : int) :
        return cls.colors[:nbre]