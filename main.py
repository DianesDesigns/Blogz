from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from main import db, Blog, User

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:MyNewPass@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_post = db.Column(db.String(1000))
    owner_id=db.column(db.Integer, db.foreign_key (user_id))

class user(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id=db.column(db.Integer, db.foreign_key (user_id))
    password=db.column(db.String(50))


    def __init__(self, blog_title, blog_post):
        self.blog_title = blog_title
        self.blog_post = blog_post


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_post = request.form['blog_post']
        new_blog = Blog(blog_title, blog_post)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/?id={0}'.format(new_blog.id))
        
    post_id = request.args.get('id')    
    if post_id:
        singlepost=Blog.query.get(post_id)
        return render_template('singlepost.html', blog = singlepost)
    
    blogs = Blog.query.all()
    return render_template('blogposts.html',title="build-a-blog", 
    blogs=blogs)
    

@app.route('/addPost', methods=['POST', 'GET'])
def addPost():

    return render_template('addPost.html')

#@app.route('/signup', methods=['POST', 'GET'])
#@app.route('/login', methods=['POST', 'GET'])
#@app.route('/index', methods=['POST', 'GET'])
#@app.route('/logout', methods=['POST'])
#def Logout():    
#    return redirect('/?blog')

if __name__ == '__main__':
    app.run()