from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://umjsrizaqqlyaaxqk4sa:p921t0GmgIYKBVsTADCZtkTgtjo9z2@bkjmaaq1ryjgctyghzs5-postgresql.services.clever-cloud.com:50013/bkjmaaq1ryjgctyghzs5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.user_id
            return redirect(url_for('dashboard'))
        flash('Nesprávny email alebo heslo.')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        new_user = User(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrácia úspešná! Teraz sa môžeš prihlásiť.')
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    offers = Offer.query.all()
    return render_template('zoznam.html', offers=offers)

@app.route('/add-offer', methods=['GET', 'POST'])
def add_offer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        user_id = session['user_id']
        new_offer = Offer(title=title, description=description, price=price, category=category, user_id=user_id)
        db.session.add(new_offer)
        db.session.commit()
        flash('Ponuka bola úspešne pridaná!')
        return redirect(url_for('dashboard'))
    return render_template('form.html')

@app.route('/rate-user/<int:user_id>', methods=['GET', 'POST'])
def rate_user(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        rating = request.form['rating']
        review = request.form['review']
        new_rating = Rating(user_id=session['user_id'], rated_user_id=user_id, rating=rating, review=review)
        db.session.add(new_rating)
        db.session.commit()
        flash('Hodnotenie bolo pridané!')
        return redirect(url_for('dashboard'))
    return render_template('newpass.html', user_id=user_id)

@app.route('/about')
def about():
    return render_template('onas.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()  # Toto vytvorí všetky tabuľky, ak ešte neexistujú
    port = int(os.environ.get('PORT', 8000))  # Nastavenie portu na 8000

