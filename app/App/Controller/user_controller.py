from App.Controller import db_postgres_controller as db

class User:
    def __init__(self,  username=None, id=None):
        self.username = username
        self.id = id
        
    # Do signup user
    def signup(self):        
        check_result = db.db.check_duplicate_id(self.id)
        if check_result is None:
            db.db.signupUser(self.username, self.id)
        return
        
