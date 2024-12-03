from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    scam_type = db.Column(db.String(100), nullable=True)
    phishing_type = db.Column(db.String(100), nullable=True)
    extortion_type = db.Column(db.String(100), nullable=True)
    incident = db.Column(db.Text)

    def __repr__(self):
        return "<Complaint {}>".format(self.id)
