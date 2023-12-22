from app import db

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    session_id = db.Column(db.String)
    question = db.Column(db.String)
    answer = db.Column(db.String)
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
    def get_by_user_id(cls, user_id, limit=10):
        return cls.query.filter_by(user_id=user_id).order_by(cls.id.desc()).limit(limit).all()

    @classmethod
    def get_by_user_id_and_partner_id(cls, user_id, partner_id, limit=10):
        return cls.query.filter_by(user_id=user_id, partner_id=partner_id).order_by(cls.id.desc()).limit(limit).all()
    
    @classmethod
    def get_by_user_id_and_session_id(cls, user_id, session_id):
        return cls.query.filter_by(user_id=user_id, session_id=session_id).order_by(cls.id.desc()).all()
    
    @classmethod
    def create(cls, user_id, partner_id, session_id, question, answer):
        call = cls(user_id=user_id, partner_id=partner_id, session_id=session_id, question=question, answer=answer)
        call.save()
        return call

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    session_id = db.Column(db.String)
    text = db.Column(db.String)
    played = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def used(self):
        self.is_used = True
        self.updated_at = db.func.now()
        db.session.commit()
    
    def play(self):
        self.played += 1
        self.updated_at = db.func.now()
        db.session.commit()
    
    @classmethod
    def get_latest_by_user_id_and_session_id(cls, user_id, session_id):
        return cls.query.filter_by(user_id=user_id, session_id=session_id).order_by(cls.id.desc()).first()
    
    @classmethod
    def create(cls, user_id, partner_id, session_id, text):
        call = cls(user_id=user_id, partner_id=partner_id, session_id=session_id, text=text)
        call.save()
        return call