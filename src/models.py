from app import db
from sqlalchemy.dialects.postgresql import JSON

class Courses(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    sln = db.Column(db.Integer)
    description = db.Column(db.String())

    def __init__(self, url, course_all):
        self.url = url
        self.course_all = course_all

    def __repr__(self):
        return f'<id {self.id}>'