

def Verification(type : str) :
    def verif(function) :
        def wrap(*args, **kwargs) :
            self = args[0]
            if type == 'precision' :
                if self.video.edit_nom_video.text.strip() == "" :
                    self.champ_nr("Nom Video")
                    return
                if self.video.edit.text().strip() == "" :
                    self.champ_nr("Lien Youtube Vide")
                    return
                
                return function(*args, **kwargs)
            return wrap
        return verif