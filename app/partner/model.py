from app import db
import re

class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identity = db.Column(db.String, unique=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    assigned_phone = db.Column(db.String, unique=True)
    address = db.Column(db.String, nullable=False)
    logo = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None, category=None, description=None, email=None, phone=None, address=None, logo=None, website=None):
        self.name = name or self.name
        self.email = (email and email.lower()) or self.email
        self.phone = phone or self.phone
        self.address = address or self.address
        self.logo = logo or self.logo
        self.category = category or self.category
        self.description = description or self.description
        self.website = website or self.website
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()
    
    def assign_phone(self, phone):
        self.assigned_phone = phone
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_by_assigned_phone(cls, assigned_phone):
        return cls.query.filter_by(assigned_phone=assigned_phone, is_deleted=False).first()
    
    @classmethod
    def get_by_identity(cls, identity):
        return cls.query.filter_by(identity=identity, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def create(cls, name, category, description, email, phone, address, logo, website):
        identity = re.sub(r'[^a-zA-Z0-9_]', '', name.lower().strip().replace(' ', '_'))
        existing = cls.get_by_identity(identity)
        if existing:
            return
        partner = cls(name=name, category=category, description=description, email=email.lower(), phone=phone, address=address, logo=logo, website=website, identity=identity)
        partner.save()
        return partner