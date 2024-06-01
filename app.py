

from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

class DataFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(120))
    filetype = db.Column(db.String(20))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return {"message": f"user {username} has been created successfully."}

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return {"message": f"Welcome, {username}!"}
    else:
        return {"message": "Invalid username or password."}

@app.route('/logout')
def logout():
    logout_user()
    return {"message": "You have been logged out."}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"message": "No file selected."}
    
    file = request.files['file']
    
    if file.filename == '':
        return {"message": "No file selected."}
    
    # Save the file to a desired location
    file.save('/path/to/save/file')
    
    return {"message": "File uploaded successfully."}

@app.route('/visualize', methods=['GET'])
def visualize_data():
    # Implement data visualization
    pass

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

@app.before_first_request
def create_tables():
    db.create_all()