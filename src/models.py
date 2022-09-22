from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    _tablename_="user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    _tablename_="people"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique = False, nullable = False)
    height = db.Column(db.Integer, unique = False, nullable = True)
    gender = db.Column(db.String(250), unique = False, nullable = True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "height": self.height,
            "gender": self.gender,
        }
class FavPeople(db.Model):
    _tablename_="favpeople"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(250), db.ForeignKey("user.email"))
    people = db.Column(db.Integer, db.ForeignKey("people.uid"))
    rel_user = db.relationship("User")
    rel_people = db.relationship("People")

    def __repr__(self):
        return '<FavPeople %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "people": self.people,
        }
class Planets(db.Model):
    _tablename_="planets"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique = True, nullable = False)
    climate = db.Column(db.String(250), unique = False, nullable = True)
    population = db.Column(db.Integer, unique = False, nullable = True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
        }
class FavPlanets(db.Model):
    _tablename_="favplanets"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(250), db.ForeignKey("user.email"))
    planets = db.Column(db.Integer, db.ForeignKey("planets.uid"))
    rel_user = db.relationship("User")
    rel_planets = db.relationship("Planets")

    def __repr__(self):
        return '<FavPlanets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "planets": self.planets,
        }