from imageboard.main import db
from datetime import date


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    head = db.Column(db.String(60), nullable=False, unique=True)
    text = db.Column(db.String(3000), nullable=False)
    date = db.Column(db.Date, default=date.today())
    comments = db.relationship('Comments', backref='art')

    def head_to_dict(self):
        return {
                self.head:self.text
                }

    def date_to_dict(self):
        return {
                self.id:self.date
                }


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.Date, default=date.today())
    art_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False, index=True)
