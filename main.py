from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random


app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()

def to_dict(cafe):

    cafes = {
        "name" : cafe.name,
        "map_url" : cafe.map_url,
        "img_url" : cafe.img_url,
        "location" : cafe.location,
        "seats": cafe.seats,
       " has_toilet" : cafe.has_toilet,
        "has_wifi":  cafe.has_wifi,
        "has_sockets": cafe.has_sockets,
        "can_take_calls": cafe.can_take_calls,
        "coffee_price": cafe.coffee_price,
    }

    return cafes


@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/random", methods=('GET')) that is possible but because get is allowed for all routs by default much simpler way is: ->
@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_cafe = random.choice(all_cafes)
    jsoned = jsonify(to_dict(random_cafe))

    
    return jsoned

@app.route("/all")
def get_all():
    all_coffee = db.session.execute(db.select(Cafe).order_by(Cafe.name)).scalars().all()
    return  jsonify(cafes=[to_dict(cafe) for cafe in all_coffee])


@app.route("/search")
def via_loc():
    query_loc = request.args.get("loc")
    via_loc = db.session.execute(db.select(Cafe).where(Cafe.location == query_loc )).scalars().all()
    if via_loc:
       return  jsonify(cafes=[to_dict(cafe) for cafe in via_loc])
    else:
        return jsonify({"error":{"Not Found": "Sorry, we don't have a cafe at that location"}})
    



# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
