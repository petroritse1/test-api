import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

 
class Config:
    load_dotenv()
    SECRET_KEY =  os.environ.get("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "new_data.db")
    SQLALCHEMY_DATABASE_URI =  os.getenv("DATABASE_URL","sqlite:///new_data.db")
    SQLALCHEMY_TRACK_MODIFICATION = False
