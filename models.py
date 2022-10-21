from app import db
from datetime import datetime

class TodoItem(db.Model):
    __tablename__ = 'todoItems'

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Task %r>' % self.id
        