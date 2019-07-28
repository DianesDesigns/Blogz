from flask import Flask, request, redirect, render_template, session, flash
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

    
   

@app.route('/', methods=['GET'])
def index():
    users=User.query.all()

    return render_template('index.html',title="Blog Users", users=users)     
    post_id = request.args.get('id')    
    if post_id:
        singlepost=Blog.query.get(post_id)
        return render_template('singlepost.html', blog = singlepost)
    
    

@app.route('/addPost', methods=['POST', 'GET'])
def addPost():
    title = ''
    post = ''
    title_error=''
    post_error=''

    if request.method=='GET':
       
        return render_template('addPost.html')
     

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_post = request.form['blog_post']    
        owner = User.query.filter_by(username = session['username']).first()
        if len(blog_title)<1:
            title_error="Please enter a title"
        if len(blog_post)<1:
            post_error="Please enter a blog post"
        if not title_error and not post_error:
            new_blog = Blog(blog_title, blog_post, owner)
            db.session.add(new_blog)
            db.session.commit()
          
            return render_template('singleUser.html', blog=new_blog)    
        #    return redirect('/blog?id={0}'.format(new_blog.id))
        else:
        
            return render_template('addPost.html', title=title,  
            title_error=title_error, post_error=post_error)

@app.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verifyPassword = request.form['VerifyPassword']

        if not username==username:
            flash('zoiks! "' + username + '" does not seem like an username')
            return redirect('/signup')
        # TODO 1: validate that form value of 'verify' matches password
        if len(username) <3 or len(username)>20:
            flash(username + "is not the correct length")
        if password == '':
            flash("please enter a password")
        if verifyPassword =='':
            flash("please verify password")
        if password != verifyPassword:
            flash("Passwords do not match")
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

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:

        return redirect('/login')    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    elif request.method == 'POST':
        password = request.form['user-password']
        username = request.form['username']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['username'] = username
                flash ("Hello," + user.username)
                return redirect('/addPost')
        flash("username or password are incorrect")
        return redirect ('/login')


@app.route('/blog', methods=['POST', 'GET'])
def blogz():
    if request.args.get('id'):
        blog_id=int(request.args.get('id'))
        info = Blog.query.get(blog_id)
        return render_template("singlepost.html", info=info)
    elif request.args.get('user'):
        blogs = Blog.query.filter_by(owner_id = request.args.get('user')).all()
        return render_template('blogposts.html', blogs=blogs)

@app.route('/allPosts', methods=['POST', 'GET'])
def showAll():
    blogs = Blog.query.all()
    return render_template('blogposts.html',title="All Posts", 
    blogs=blogs)


#@app.route('/index', methods=['POST', 'GET'])
@app.route('/logout')
def Logout():    
    del session ['username']
    return redirect('/blog')

if __name__ == '__main__':
    app.run()