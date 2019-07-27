from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:MyNewPass@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Ab@CD#efG'




class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password=db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
    

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_post = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey ('user.id'))

    def __init__(self, blog_title, blog_post, owner):
        self.blog_title = blog_title
        self.blog_post = blog_post
        self.owner = owner

    
   

@app.route('/', methods=['POST', 'GET'])
def index():

           
    post_id = request.args.get('id')    
    if post_id:
        singlepost=Blog.query.get(post_id)
        return render_template('singlepost.html', blog = singlepost)
    
    blogs = Blog.query.all()
    return render_template('blogposts.html',title="build-a-blog", 
    blogs=blogs)
    

@app.route('/addPost', methods=['POST', 'GET'])
def addPost():
    if request.method == 'POST':
        owner = User.query.filter_by(username = session['username']).first()
        blog_title = request.form['blog_title']
        blog_post = request.form['blog_post']
        new_blog = Blog(blog_title, blog_post, owner)
        db.session.add(new_blog)
        db.session.commit()
        blog_id = new_blog.id
        return redirect('/blog?id={0}'.format(new_blog.id))

    return render_template('addPost.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #if not username==username:
        #    flash('zoiks! "' + username + '" does not seem like an username')
        #    return redirect('/signup')
        # TODO 1: validate that form value of 'verify' matches password
        # TODO 2: validate that there is no user with that username already
        #user = User(username=username)
        existing_user = User.query.filter_by(username = username).first()
        if not existing_user:
            user=User(username, password)  
            db.session.add(user)
            db.session.commit()
            session['username'] = username
            return redirect('/addPost')
        else:
            return render_template('signup.html')
    return render_template('signup.html')

    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    elif request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['username'] = username
                flash ("Hello," + user.username)
                return redirect('/newpost')
        flash("username or password are incorrect")
        return redirect ('/login')


@app.route('/blog', methods=['POST', 'GET'])
def blogz():
    if request.args.get('id'):
        blog_id=int(request.args.get('id'))
        info = Blog.query.get(blog_id)
        return render_template("singlepost.html", info=info)
    else:


        blogs = User.query.all()
        return render_template('blogposts.html', blogs=blogs)


#@app.route('/index', methods=['POST', 'GET'])
@app.route('/logout')
def Logout():    
    del session ['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()