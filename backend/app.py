from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET-KEY'] = 'dsfmakdf'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

with app.app_context():
    db.create_all()
    users = User.query.all()
    print("hey", users)

@app.route("/login")
def login():
    return "log in"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8085)
