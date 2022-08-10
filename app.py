


from flask import Flask,render_template ,request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,logout_user
from datetime import datetime

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb2.db'
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

class Blog(db.Model):
    title=db.Column(db.String(80),nullable=False)
    blog_id=db.Column(db.Integer, primary_key=True)
    author=db.Column(db.String(80),nullable=False)
    content=db.Column(db.Text(),nullable=False)
    pub_date=db.Column(db.DateTime(),nullable=False,default=datetime.utcnow())
    
    def __repr__(self):
        return '<Blog %r>' % self.title


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/main")
def main():
    return render_template("main.html") 

@app.route("/")
def index():
    data = []
    return render_template("index.html",data=data)
  

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        username=request.form.get('uname')
        fullname=request.form.get('fullname')
        user = User(
            username=username, 
            email=email, 
            name=fullname,
            password=password
        )
       

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
        
        if user and password==user.password:
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid credentials','danger')
            return redirect('/login')

    return render_template("login.html")  

@app.route("/Logout")
def logout():
    logout_user()
    return redirect('/')

@app.route("/blogpost",methods=['GET','POST'])
def blogpost():
    if request.method=='POST':
        title=request.form.get('title')
        author= request.form.get('author')
        content= request.form.get('content')
        pub_date = datetime.now()
        blog=Blog(title=title,author=author,content=content, pub_date=pub_date)
        db.session.add(blog)
        db.session.commit()
        flash("your post has been submitted sucessfuly",'sucess')
        return redirect('/')

    return render_template('/blog.html')

if __name__=="__main__":
    
    app.run(debug=True)
