from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rentals.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# =========================
# DATABASE MODELS
# =========================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    location = db.Column(db.String(200))
    rent = db.Column(db.Integer)
    deposit = db.Column(db.Integer)
    description = db.Column(db.Text)


class Dispute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.String(500))
    status = db.Column(db.String(50), default='Open')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# =========================
# LOGIN MANAGER
# =========================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =========================
# ROUTES
# =========================

@app.route('/')
def index():
    listings = Listing.query.all()
    return render_template('index.html', listings=listings)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    app.run(debug=True)