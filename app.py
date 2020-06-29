from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(30), nullable = False, default = 'Unknown')
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
   
    def __repr__(self):
        return f'Blog Post {self.id}'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts')
def posts():
    all_posts = BlogPost.query.order_by(BlogPost.date).all()
    return render_template('posts.html', posts = all_posts)

@app.route('/<string:name>')
def helloName(name):
    return "Hello {}".format(name)

# @app.route('/langoorMithi')
# def hello():
#     return "Hello World"

@app.route('/getonly', methods = ['GET'])
def get_req():
    return 'You only get this webpage.'

@app.route('/posts/delete/<int:id>')
def delete(id):
    db.session.delete(BlogPost.query.get(id))
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/<int:id>')
def content(id):
    post = BlogPost.query.get(id)
    return render_template('content.html', post = post)

@app.route('/posts/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get(id)

    if request.method == 'GET':
        return render_template('edit.html', post = post)
    
    else:
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        post.author = 'Unknown' if post.author == '' else post.author
        db.session.commit()
        return redirect(f'/posts/{id}')

@app.route('/posts/new-post', methods = ['GET', 'POST'])
def newPost():
    if request.method == 'GET':
        return render_template('new-post.html')
    
    else:
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        author = 'Unknown' if author == '' else author
        post = BlogPost(title = title, content = content, author = author)
        db.session.add(post)
        db.session.commit()
        return redirect('/posts')

if __name__ == '__main__':
    app.run(debug = True)
