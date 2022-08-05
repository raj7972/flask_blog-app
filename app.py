
from unicodedata import name
from flask import Flask,render_template ,request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120),  nullable=False)
    password = db.Column(db.String(120),  nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/main")
def main():
    return render_template("main.html") 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        username=request.form.get('uname')
        fullname=request.form.get('fullname')
        user = User(username=username, email=email, name=fullname,
         password=password)
       

        db.session.add(user)
        db.session.commit()
        flash('user has been registered sucessfully','success')
        return redirect('/login')


    return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        print("Form variables:", request.form.keys())
        username=request.form.get('username')
        password=request.form.get('password')
        user=User.query.filter_by(username=username).first()
        
        print(username)
        print(password)
        if user:
            print(user.username)
            print(user.password)
        else:
            print("User not found")
        if user and password==user.password:
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid credentials','warning')
            return redirect('/login')

    return render_template("login.html")



if __name__=="__main__":
    
    app.run(debug=True)
