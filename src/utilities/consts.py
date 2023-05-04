from flask_sqlalchemy import SQLAlchemy
from flask_session import Session


DB_Name = "project.db"
db = SQLAlchemy()
sess = Session()
