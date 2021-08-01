from src.database.db import db


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    college_id = db.Column(
        db.Integer, db.ForeignKey('college.id', use_alter=True), nullable=False)
    departments = db.relationship(
        'Department', lazy='select', backref=db.backref('faculty', lazy='joined'))
    dean_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', use_alter=True), nullable=False)

    def __repr__(self):
        return '<Faculty %r>' % self.name

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
        faculty = {
            'id': self.id,
            'name': self.name,
            'college_id': self.college_id,
            'dean_id': self.dean_id,
        }
        return faculty
