import secrets

class AdminUser():

    # construct / attributes
    def __init__(self, username):
        self.id = secrets.token_hex(16)
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = True


    @staticmethod
    def login():
       return True

    def __str__(self):
        return f'Id: {self.id}\nUsername: {self.username}\n'

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.is_authenticated

    def is_anonymous(self):
        return True
        
    def get(self,id):
        return self
    
    def get_id(self):
        return self.id