from src.database.db import db


class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    provost_id = db.Column(db.Integer, db.ForeignKey('user.id', use_alter=True), nullable=True)
    faculties = db.relationship("Faculty", lazy='select', backref=db.backref('college', lazy='joined'))
    other_users = db.relationship("OtherUser", lazy='select', backref=db.backref('college', lazy='joined'))

    def __repr__(self):
        return '<College %r>' % self.name

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        college = {
            'id': self.id,
            'name': self.name,
            'provost_id': self.provost_id
        }
        return college
