"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Tags, Articles, ArticlesTags, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints

#Users
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def all_users():
    data = Users.query.all()
    data = [user.serialize() for user in data]

    return jsonify({"msg": "OK", "data": data})

@app.route('/users', methods=['POST'])
def create_users():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email or not password:
        return jsonify({"msg": 'todos los datos son necesarios'}), 400
    
    check = Users.query.filter_by(email=email).first()
    if check:
        return jsonify({"msg": 'correo ya existe, inicia sesion'}), 400

    # Crear el nuevo usuario
    new_user = Users(email=email, password=password, is_active=True)
    
    # Agregar el nuevo usuario a la base de datos
    db.session.add(new_user)
    db.session.commit()

    # Devolver el nuevo usuario como JSON (usando serialize)
    return jsonify({"msg" : "OK", "data" : new_user.serialize()})


# Tags
@app.route('/tags', methods=['GET'])
def all_tags():
    data = Tags.query.all()
    data = [tag.serialize() for tag in data]
    return jsonify({"msg": "OK", "data": data})



#Articles
@app.route('/articles', methods=['GET'])
def all_articles():
    articles = Articles.query.all()
    print(articles)
    articles = [article.serialize() for article in articles]
    return jsonify({"msg": "OK", "data": articles})


@app.route('/articles/<int:id>', methods=['GET'])
def one_article(id):
    article = Articles.query.get(id)
    print(article)
    return jsonify({"msg": "one article with id:" + str(id), "article": article.serialize()})


@app.route('/articles', methods=['POST'])
def create_article():
    title = request.json.get('title', None)
    content = request.json.get('content', None)
    user_id = request.json.get('user_id', None)

    if not title or not content or not user_id:
        return jsonify({"msg": 'todos los datos son necesarios'}), 400
    
    data = Articles(title=title, content=content, user_id=user_id)
    db.session.add(data)
    db.session.commit()

    check = Users.query.filter_by(title=title)
    
    return jsonify({"msg": "get all articles"})


# ArticlesTags

@app.route('/articlesTags', methods=['POST'])
def create_articleTags():
    title = request.json.get('title', None)
    content = request.json.get('content', None)
    user_id = request.json.get('user_id', None)

    if not title or not content or not user_id:
        return jsonify({"msg": 'todos los datos son necesarios'}), 400
    
    data = Articles(title=title, content=content, user_id=user_id)
    db.session.add(data)
    db.session.commit()

    check = Users.query.filter_by(title=title)
    
    return jsonify({"msg": "get all articles"})


#Planets
@app.route('/planets', methods=['GET'])
def all_planets():
    data = Planets.query.all()
    data = [planet.serialize() for planet in data]
    return jsonify({"msg": "OK", "data": data})



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
