'''
Main app/routing file for Twitoff
'''

from flask import Flask, render_template
from .models import DB, User

def create_app():
    '''
    Creates and Configures a Flask Application
    '''
    app = Flask(__name__)
    # store information locally
    app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # connect database to app.py file
    DB.init_app(app)


    # rest of code for app
    @app.route('/') # @ is a decorator
    def root():
        # run a query
        users = User.query.all() # returns all the users
        return render_template('base.html',
                                title= 'Home',
                                users = User.query.all(),
                                )


    return app