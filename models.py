from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    professional = db.relationship('Professional', backref='user', uselist=False,
                                   cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy='dynamic',
                              cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Professional(db.Model):
    __tablename__ = 'professionals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, default='')
    experience = db.Column(db.String(50), default='')
    image = db.Column(db.String(256), default='default.png')
    approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship('Review', backref='professional', lazy='dynamic',
                              cascade='all, delete-orphan')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    @property
    def review_count(self):
        return self.reviews.count()

    def __repr__(self):
        return f'<Professional {self.full_name}>'


CATEGORIES = [
    ('hidraulik', 'Hidraulik'),
    ('elektricist', 'Elektricist'),
    ('mekanik', 'Mekanik'),
    ('piktor', 'Piktor'),
    ('fotograf', 'Fotograf'),
    ('programues', 'Programues'),
    ('kondicionim', 'Teknik Kondicionimi'),
    ('pastrim', 'Shërbime Pastrimi'),
    ('mobileri', 'Specialist Mobiliesh'),
]

CITIES = [
    'Tiranë', 'Durrës', 'Vlorë', 'Elbasan', 'Shkodër',
    'Fier', 'Korçë', 'Berat', 'Lushnjë', 'Pogradec',
    'Kavajë', 'Gjirokastër', 'Sarandë', 'Lezhë', 'Kukës',
    'Peshkopi', 'Burrel', 'Përmet', 'Tepelenë', 'Gramsh',
]


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.rating}* by User {self.user_id}>'
