from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from geopy import Yandex

place = ""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), nullable=False)
    roof_type = db.Column(db.String(15), nullable=False)
    expenses = db.Column(db.Integer)
    economy = db.Column(db.Integer)
    shirota = db.Column(db.Float)
    dolgota = db.Column(db.Float)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == "POST":
        address = request.form['address']
        roof_type = request.form['roof_type']
        expenses = request.form['expenses']
        economy = request.form['economy']

        article = Article(address=address, roof_type=roof_type, expenses=expenses, economy=economy)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/reg1')
        except:
            return "При вводе данных произошла ошибка"
    else:
        return render_template("reg.html")


@app.route('/reg1')
def reg1():
    place = Article.query.order_by(Article.id.desc()).first()
    place = place.address
    location = Yandex(api_key='1ee7a6da-d560-42e1-b26e-03c85a5832ad').geocode(place)

    print(location.address)
    print(location.latitude, location.longitude)

    loc = [location.latitude, location.longitude]
    return render_template("reg1.html", loc)


if __name__ == "__main__":
    app.run(debug=True)