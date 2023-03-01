from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate, migrate

# migrate = Migrate(app, db)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"


@app.route("/")
def index():
    
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)


@app.route("/add_data")
def add_data():
    return render_template('add_profile.html')

@app.route("/add", methods=["POST"])
def profile():

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")   


    if first_name != '' and last_name != '' and age is not None:
        p = Profile(first_name=first_name, last_name=last_name, age=age)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/delete/<int:id>')
def erase(id):
    profile = Profile.query.get_or_404(id)

    try:
        db.session.delete(profile)
        db.session.commit()
        return redirect('/')
    except:
        return "When deleting article happen error"

if __name__ == '__main__':
    app.run(debug=True)