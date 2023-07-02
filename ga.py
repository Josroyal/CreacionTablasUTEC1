# IMPORTS
from flask import Flask,render_template,jsonify,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
import sys
from flask_migrate import Migrate
import os
from flask_login import login_user,login_required,current_user,LoginManager,UserMixin, logout_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:josue2003@localhost:5432/skinloot"
app.config['UPLOAD_FOLDER'] = 'static/usuarios'
app.secret_key = 'clave'
db = SQLAlchemy(app)






with app.app_context():db.create_all()

# CORRER LA APP
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))

