

class decorator :
    @staticmethod
    def youtube_verification(function) :
        def wrap(self, **kwargs) :
                if self.youtube_interface.barr.path_folder.strip() == "" :
                    self.champ_warning("Emplacement vide", "Il est impératif\n de choisir l'emplacement du fichier")
                    return
                elif self.youtube_interface.barr.edit_nom_video.text().strip() == "" :
                    self.champ_warning("Lien Nom vide", "Il est obligatoire de\nRemplir le champ Nom Vidéo")
                    return
                elif self.youtube_interface.barr.edit.text().strip() == "" :
                    self.champ_warning("Lien Youtube Nom Rempli", "Il est impératif de remplir\n Le champ Lien Youtube")
                    return
                
                return function(self, **kwargs)
        return wrap
    
    @staticmethod
    def precision_verification(function) :
        def wrap(self, **kwargs) :
            indexeur = self.youtube_interface.precision if function.__name__ == "slots_youtube_srt_generate" else self.video_retranscribe_interface.precision
            if indexeur.video.name.text().strip() == "":
                self.champ_warning("Attention", "Il est impératif de remplir\n Le Nom du Fichier")
                return
            elif indexeur.video.precision.text().strip() == "" :
                self.champ_warning("Attention", "Il est impératif de remplir\n la précision")
                return
            elif indexeur.video.path_srt.strip() == "" :
                self.champ_warning("Attention", "Il est impératif de sélectionner\n le dossier de destination du srt")
                return
            return function(self, **kwargs)
        
        return wrap
    
    @staticmethod
    def audio_extract_verification(function) :
        def wrap(self, **kwargs) :
            if self.path.strip() == "" :
                self.warning(
                    "Error",
                    "Sélectionnez la vidéo à \nRetranscrire"
                )
                return
            if self.path_audio.strip() == "" :
                self.warning(
                    "Error",
                    "Sélectionnez l'url de l'audio \nextrait.."
                )
                return
            if self.name.text().strip() == "" :
                self.warning(
                    "Error",
                    "Entrer le nom de l'audio extrait.."
                )
                return
            return function(self, **kwargs)
        return wrap