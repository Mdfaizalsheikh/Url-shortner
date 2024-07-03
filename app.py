from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    link = URL.query.filter_by(short_url=short_url).first()
    if link:
        return generate_short_url()
    return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        existing_url = URL.query.filter_by(long_url=long_url).first()
        if existing_url:
            return f'Short URL is: {request.url_root}{existing_url.short_url}'
        short_url = generate_short_url()
        new_url = URL(long_url=long_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return f'Short URL is: {request.url_root}{short_url}'
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    link = URL.query.filter_by(short_url=short_url).first_or_404()
    link.clicks += 1
    db.session.commit()
    return redirect(link.long_url)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
