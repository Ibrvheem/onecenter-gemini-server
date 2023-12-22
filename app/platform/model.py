import bcrypt
from app import db

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username, is_deleted=False).first()
    
    @classmethod
    def is_authorized(cls, username, password):
        platform = cls.get_by_username(username)
        if platform:
            return bcrypt.checkpw(password.encode('utf-8'), platform.password.encode('utf-8'))
        return False
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def create(cls, name, username, password):
        platform = cls(name=name, username=username, password=password)
        platform.password = bcrypt.hashpw(platform.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        platform.save()
        return platform