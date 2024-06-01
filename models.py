from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)
    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete')

    def to_dict(self, include_powers=False):
        hero_dict = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }
        if include_powers:
            hero_dict['hero_powers'] = [hp.to_dict() for hp in self.hero_powers]
        return hero_dict

class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    @validates('strength')
    def validate_strength(self, key, strength):
        assert strength in ['Strong', 'Weak', 'Average'], 'Strength must be one of: Strong, Weak, Average'
        return strength

    @validates('power_id')
    def validate_power_id(self, key, power_id):
        power = Power.query.get(power_id)
        assert power, 'Power not found'
        return power_id

    @validates('hero_id')
    def validate_hero_id(self, key, hero_id):
        hero = Hero.query.get(hero_id)
        assert hero, 'Hero not found'
        return hero_id

    def to_dict(self):
        return {
            'id': self.id,
            'strength': self.strength,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'hero': self.hero.to_dict(),
            'power': self.power.to_dict()
        }
