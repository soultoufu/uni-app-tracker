from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Not Submitted')  # E.g., Submitted, Interview, Offer, Rejected
    deadline = db.Column(db.String(50))
    notes = db.Column(db.Text)
