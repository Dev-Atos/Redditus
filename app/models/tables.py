from app import db, lm


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def get_id(self):
        return str(self.id)
    
    @lm.user_loader
    def load_user(self):
     return Users.get(self.id)


    def __self__(self, username, email, password): #Para ser possível a instanciação de classe
        self.username = username
        self.email = email
        self.password = password