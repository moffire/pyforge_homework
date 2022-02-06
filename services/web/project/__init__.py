from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class SuperHeroes(db.Model):
    __tablename__ = 'superheroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    power = db.Column(db.Integer, db.CheckConstraint('0 < power'), nullable=False)
    is_villain = db.Column(db.Boolean, nullable=False)
    deceased_date = db.Column(db.Date, nullable=True)
    chronicle = relationship('Chronicles', cascade='all, delete')

    def to_dict(self):
        return {attr.key: getattr(self, attr.key) for attr in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f'name: {self.name}, power: {self.power}'


class Chronicles(db.Model):
    __tablename__ = 'chronicles'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('superheroes.id'))
    year = db.Column(db.Integer, db.CheckConstraint('2000 <= year'))
    text = db.Column(db.Text)

    def to_dict(self):
        return {attr.key: getattr(self, attr.key) for attr in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f'name: {self.superhero.name}, text: {self.text}'


@app.route("/")
def main_page():
    superheroes = []
    chronicles = []

    for hero in SuperHeroes.query.all():
        superheroes.append(hero.to_dict())

    for chronicle in Chronicles.query.all():
        chronicles.append(chronicle.to_dict())

    return jsonify(superheroes=superheroes, chronicles=chronicles)
