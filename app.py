#app setup
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

#init the database
db = SQLAlchemy()



def page_not_found(e):
    return render_template('404.html'), 404

def internal_server_error(e):
    return render_template('500.html'), 500

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'shuajayshujay'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qglkftgvmsbymz:4785be4a75bd04b266f95eba14f1d662fe7c5a4f1ab5246d624cf7847c5b3e8c@ec2-3-213-66-35.compute-1.amazonaws.com:5432/d3n9cd42a7lq3j'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///librarymanagement.sqlite'
    
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

    #error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    return app