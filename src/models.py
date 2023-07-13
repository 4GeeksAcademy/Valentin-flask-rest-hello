from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    surname = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    inscription_date = db.Column(db.String(250), nullable=False)
    addresses = db.relationship('Address', backref='user')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "surname": self.surname,
            "phone_number": self.phone_number,
            "email": self.email,
            "inscription_date": self.inscription_date
        }

    def to_dict(self):
        return self.serialize()


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(250))
    street_number = db.Column(db.String(250))
    postal_code = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super(Address, self).__init__(**kwargs)

    def __repr__(self):
        return '<Address %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "street_name": self.street_name,
            "street_number": self.street_number,
            "postal_code": self.postal_code,
            "user_id": self.user_id
        }

    def to_dict(self):
        return self.serialize()


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(250))
    size = db.Column(db.Integer)
    favorite = db.relationship('FavoriteList', backref='planet')

    def __init__(self, **kwargs):
        super(Planet, self).__init__(**kwargs)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "size": self.size,
            "favorite_list_id": self.favorite_list_id
        }

    def to_dict(self):
        return self.serialize()


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(250))
    age = db.Column(db.Integer)
    weapon = db.Column(db.String(250))
    favorite = db.relationship('FavoriteList', backref='character')

    def __init__(self, **kwargs):
        super(Character, self).__init__(**kwargs)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "age": self.age,
            "weapon": self.weapon,
            "favorite_list_id": self.favorite_list_id
        }

    def to_dict(self):
        return self.serialize()


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.String(250))
    age = db.Column(db.Integer)
    weapon = db.Column(db.String(250))
    favorite = db.relationship('FavoriteList', backref='vehicle')

    def __init__(self, **kwargs):
        super(Vehicle, self).__init__(**kwargs)

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "age": self.age,
            "weapon": self.weapon,
            "favorite_list_id": self.favorite_list_id
        }

    def to_dict(self):
        return self.serialize()


class FavoriteList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super(FavoriteList, self).__init__(**kwargs)

    def __repr__(self):
        return '<FavoriteList %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            "vehicle_id": self.vehicle_id,
            "user_id": self.user_id
        }

    def to_dict(self):
        return self.serialize()
