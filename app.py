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
        role = request.form['role']

        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')

    return render_template('login.html')
@app.route('/dashboard')
@login_required
def dashboard():
    disputes = Dispute.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', disputes=disputes)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create_listing', methods=['GET', 'POST'])
@login_required
def create_listing():

    if current_user.role != 'owner':
        flash('Only owners can create listings')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        listing = Listing(
            title=request.form['title'],
            location=request.form['location'],
            rent=request.form['rent'],
            deposit=request.form['deposit'],
            description=request.form['description']
        )

        db.session.add(listing)
        db.session.commit()

        flash('Listing created successfully!')
        return redirect(url_for('index'))

    return render_template('create_listing.html')


@app.route('/listings')
def listings():
    listings = Listing.query.all()
    return render_template('listings.html', listings=listings)


@app.route('/dispute', methods=['GET', 'POST'])
@login_required
def dispute():

    if request.method == 'POST':
        issue = request.form['issue']

        new_dispute = Dispute(
            issue=issue,
            user_id=current_user.id
        )

        db.session.add(new_dispute)
        db.session.commit()

        flash('Dispute submitted successfully!')
        return redirect(url_for('dashboard'))

    return render_template('dispute.html')


# =========================
# MAIN
# =========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)