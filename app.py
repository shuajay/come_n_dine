#app setup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

#init the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'shuajayshujay'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///librarymanagement.sqlite'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mciuzicxnqimtn:303c9810cbf0202712d0caecd5cc7ffb8777caa0aeea51b99fc924748f64d4be@ec2-35-170-146-54.compute-1.amazonaws.com:5432/d98v5s7g749l96'
    

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader #tells Flask-login how to load users given an id
    def load_user(id):
        
        #since user_id is the primary key of user table use it in query
        return User.query.get(int(id))

    #blueprints for the authentication methods
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #blueprint for non auth operations
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app