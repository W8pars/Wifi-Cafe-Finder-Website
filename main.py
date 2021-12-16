from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # create/return dict object to later jsonify
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


def make_bool(val: int) -> bool:
    return bool(int(val))


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/all_cafes')
def show_all_cafes():
    cafes = db.session.query(Cafe).all()
    cafe_list = [cafe.to_dict() for cafe in cafes]
    return render_template('all_cafes.html', cafe_list=cafe_list)


@app.route('/about')
def about():
    return render_template('about.html')


# HTTP POST - Create Record
@app.route('/add', methods=['GET', 'POST'])
def add_new_cafe():
    if request.method == 'POST':
        cafe_name = request.form['name']
        map_url = request.form['map_url']
        img_url = request.form['img_url']
        location = request.form['location']
        has_sockets = make_bool(request.form['has_sockets'])
        has_toilet = make_bool(request.form['has_toilet'])
        has_wifi = make_bool(request.form['has_wifi'])
        can_take_calls = make_bool(request.form['can_take_calls'])
        seats = request.form['seats']
        coffee_price = request.form['coffee_price']
        new_cafe = Cafe(
            name=cafe_name,
            map_url=map_url,
            img_url=img_url,
            location=location,
            has_sockets=has_sockets,
            has_toilet=has_toilet,
            has_wifi=has_wifi,
            can_take_calls=can_take_calls,
            seats=seats,
            coffee_price=coffee_price,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_cafe.html')


if __name__ == '__main__':
    app.run(debug=True)
