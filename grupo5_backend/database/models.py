# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime

from grupo5_backend.database import db

# TABLA QUE RELACIONA POSTS-USUARIOS MANY TO MANY PARA SUBSCRIPCION
subs = db.Table('subs',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('post_id',db.Integer,db.ForeignKey('post.id')),
    )



#MODELO DE POSTS
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable = False)
    body = db.Column(db.Text)
    published_at = db.Column(db.DateTime)
    author_name = db.Column(db.String(80))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    #Se relaciona con la tabla users de manera que users tenga muchos posts pero post solo un author
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))


    def __init__(self, title, body, category,user, published_at=None):
        self.title = title
        self.body = body
        if published_at is None:
            published_at = datetime.utcnow()
        self.published_at = published_at
        self.category = category
        self.author = user
        self.author_name = user.name

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

#MODELO DE USERS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    name = db.Column(db.String(80), nullable = False)
    password = db.Column(db.String(80), nullable = False)
    created_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    #Se crea relacion many to many con posts para subscripcion
    subcriptions = db.relationship('Post', secondary=subs, backref=db.backref('subscribers'), lazy='dynamic')
    

    def __init__(self, email,name,password,subcription_id,created_at,update_at):
        self.email = email
        self.name = name
        self.password = password
        self.subcription_id = subcription_id
        self.created_at = created_at
        self.update_at = update_at
    
    def __repr__(self):
        return '<User %r>' % self.name

#MODELO DE MESSAGES
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable = False)
    published_at = db.Column(db.DateTime)
    author_name = db.Column(db.String(80))

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('messages', lazy='dynamic'))

    #Se relaciona con la tabla post de manera que post tenga muchos messages pero message solo un post
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref=db.backref('messages', lazy='dynamic'))

    def __init__(self, title, body, category,user, post, published_at=None):
        self.body = body
        if published_at is None:
            published_at = datetime.utcnow()
        self.published_at = published_at
        self.author = user
        self.author_name = user.name
        self.post = post

    def __repr__(self):
        return '<Message %r>' % self.title

#MODELO DE REPLIES
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable = False)
    published_at = db.Column(db.DateTime)
    author_name = db.Column(db.String(80))

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('replies', lazy='dynamic'))

    #Se relaciona con la tabla messages de manera que messages tenga muchos replies pero reply solo un message
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    message = db.relationship('Message', backref=db.backref('replies', lazy='dynamic'))

    def __init__(self, title, body, category,user, message, published_at=None):
        self.body = body
        if published_at is None:
            published_at = datetime.utcnow()
        self.published_at = published_at
        self.author = user
        self.author_name = user.name
        self.message = message

    def __repr__(self):
        return '<Reply %r>' % self.title


