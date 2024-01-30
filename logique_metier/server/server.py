import requests, mimetypes
from requests.exceptions import InvalidSchema

class requester :
    def __init__(self, url : str, port : int) :
        self.url = url + ':' + str(port)

    def send_file(self, url_path : str, endpoint : str, data_1 : dict[str, str]) -> requests.Response :
        files = {'file' : open(url_path, "rb")}   
        data = {'name' : url_path.split('/')[-1]}
        if len(data_1) != 0 :  
            data.update(data_1)
            print(data)
        reponse = requests.post(self.url + '/' + endpoint, files = files, data = data)
        return reponse
    
    def send_auth(self, endpoint : str, data : dict[str, str]) :
        response = requests.post(self.url + '/' + endpoint, data = data)
        res = response.json()
        return res
    
    def send_new_user_data(self, name: str, password : str, email : str, age : int, endpoint : str) -> dict: 
        data = {
            'name' : name,
            'password' : password,
            'mail' : email,
            'age' : str(age)
        }
        response = requests.post(self.url + '/' + endpoint, data = data)
        data = response.json()
        return data

    def receive_file(self, endpoint : str, name : str, extension : str, path : str) :
        data = requests.get(self.url + '/' + endpoint)
        print("path non acc : ", path)
        open(path + "/" + name + "." + extension, 'wb').write(data.content)
        return data
    
    def recharger_compte(self, endpoint : str, montant : float, id : int) :
        response = requests.post(self.url + '/' + endpoint, data = {'montant' : montant, "id" : id})
        return response
    
    def changer_mot_de_passe(self, email : str, endpoint : str, last_password : str, new_password : str) :
        response = requests.post(self.url + '/' + endpoint, data = {"email" : email, "last_password" : last_password, "new_password" : new_password})
        return response

    def get_user_by_mail(self, endpoint : str, email : str) :
        user = requests.post(self.url + '/' + endpoint, data = {'mail' : email})
        data = user.json()
        return {
            "name" : data['name'],
            "mail" : data['mail'],
            'compte' : data['compte'],
            'age' : data['age'],
            'id' : data['id']
        }
    
