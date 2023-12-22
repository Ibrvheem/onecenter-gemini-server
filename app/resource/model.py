from app import db

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    url = db.Column(db.String)
    training_status = db.Column(db.String)
    description = db.Column(db.String)
    partner_id = db.Column(db.Integer, db.ForeignKey("partner.id"))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, title=None, url=None, description=None, training_status=None):
        self.title = title or self.title
        self.url = url or self.url
        self.description = description or self.description
        self.training_status = training_status or self.training_status
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
    def get_by_url(cls, url):
        return cls.query.filter_by(url=url, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def get_by_partner_id(cls, partner_id):
        return cls.query.filter_by(partner_id=partner_id, is_deleted=False).all()
    
    @classmethod
    def create(cls, title, description, url, partner_id):
        resource = cls(title=title, description=description, url=url, partner_id=partner_id)
        resource.save()
        return resource