from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))  # INCREASED FROM 128 TO 255
    role = db.Column(db.String(10), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    dob = db.Column(db.Date)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    
    # Document fields
    aadhar_front = db.Column(db.String(255))
    aadhar_back = db.Column(db.String(255))
    license = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    application_status = db.Column(db.String(20), default='Pending')

    user = db.relationship('User', backref='agent', uselist=False)
