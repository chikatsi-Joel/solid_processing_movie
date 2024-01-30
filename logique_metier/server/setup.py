

url = ""
port = 5000

def get_type_by_precision(value : int) :
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
        