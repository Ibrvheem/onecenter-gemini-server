from app import db

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    partner_id = db.Column(db.Integer, db.ForeignKey("partner.id"))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None, phone=None):
        self.name = name or self.name
        self.phone = phone or self.phone
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
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def get_all_by_partner_id(cls, partner_id):
        return cls.query.filter_by(is_deleted=False, partner_id=partner_id).all()
    
    @classmethod
    def create(cls, name, email, phone, partner_id, user_id):
        agent = cls(name=name, email=email.lower(), phone=phone, partner_id=partner_id, user_id=user_id)
        agent.save()
        return agent