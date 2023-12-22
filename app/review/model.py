from app import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    company = db.Column(db.String)
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None, email=None, company=None, content=None):
        self.name = name or self.name
        self.email = email or self.email
        self.company = company or self.company
        self.content = content or self.content
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
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.is_deleted==False, cls.content!='', cls.content!=None).all()
    
    @classmethod
    def create(cls, name, email, company, content=None):
        review = cls(name=name, email=email, company=company, content=content)
        review.save()
        return review