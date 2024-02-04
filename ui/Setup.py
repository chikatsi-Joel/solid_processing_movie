import string, random



class Setup :

    format = [
        "mp3",
        "wav"
    ]
    lang = {
            'anglais' : 'en',
            'français' : 'fr',
            'russe' : 'ru',
            'protugais' : 'pt',
            'allemand' : 'de',
            'italien' : 'it',
            'japonais' : 'ja',
            'chinois' : 'zh'
    }
    
    def Convert(value : int) :
        if value <= 20 :
            return 'tiny'
        elif value <= 40: 
            return 'base'
        elif value <= 60 : 
            return 'small'
        elif value <= 80: 
            return 'medium'
        elif value <= 100 : 
            return 'large'
        
    def tarif(value : int) :
        if value < 60 :
            return 0
        elif value < 80 :
            return 4
        else:
            return 8
        
    def get_url() -> str:
        return "http://127.0.0.1"
    
    def get_port() -> int :
        return 5000
        
    def generate_name(number : int) :
        return ''.join([string.ascii_letters[random.randint(0, 10)]+str(random.randint(0, 5)) for _ in range(number)])

    