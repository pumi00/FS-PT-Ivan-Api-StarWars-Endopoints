from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ArticlesTags(db.Model):
    __tablename__= 'articleTags'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    extra_info = db.Column(db.String(100))

    def __repr__(self):
        return '<ArticlesTags %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "article_id": self.article_id,
            "tag_id": self.tag_id,
            "extra_info": self.extra_info
            # do not serialize the password, its a security breach
        }
    




class Users(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    articles = db.relationship('Articles', backref='user')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "articles": [article.serialize() for article in self.articles] if self.articles else None
            # do not serialize the password, its a security breach
        }
    

class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.relationship('Tags', secondary='articleTags', backref='articles')


    def __repr__(self):
        return '<Articles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "tags": [tag.serialize() for tag in self.tags] if self.tags else None
            # do not serialize the password, its a security breach
        }


class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(80), unique=False, nullable=False)


    def __repr__(self):
        return '<Tags %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "tag": self.tag,
            # do not serialize the password, its a security breach
        }

#Planets

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    planets = db.Column(db.String(80), nullable=False, unique=False)
    types = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planets": self.planets,
            "types" : self.types
            
        }
    


class Peoples(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    people = db.Column(db.Integer, nullable=False, unique=False)
    age = db.Column(db.String(80), unique=False, nullable=False)
    specie = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "people": self.people,
            
        }
    

