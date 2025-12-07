from app import db
from datetime import datetime

class Currency(db.Model):
    __tablename__ = 'currencies'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)  # USD, EUR, UAH
    name = db.Column(db.String(50), nullable=False)
    
    users = db.relationship('User', back_populates='default_currency')
    records = db.relationship('Record', back_populates='currency')

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    default_currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=True)
    
    default_currency = db.relationship('Currency', back_populates='users')
    records = db.relationship('Record', back_populates='user', cascade='all, delete-orphan')

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    records = db.relationship('Record', back_populates='category', cascade='all, delete-orphan')

class Record(db.Model):
    __tablename__ = 'records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    user = db.relationship('User', back_populates='records')
    category = db.relationship('Category', back_populates='records')
    currency = db.relationship('Currency', back_populates='records')
