"""
Initialise extensions: SQLAlchemy and Flask extensions.
"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
