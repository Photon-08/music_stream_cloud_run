import os
from flask import Flask, session
from applications import config
from applications.config import LocalDevelopmentConfig
from applications.database import db 
#from applications.controllers import *
#from flask_session import Session


app = None

def create_app():
    app = Flask(__name__,template_folder='templates')

    if os.getenv("ENV", "development") == "Prod":
        raise Exception("Prod Environment is not avaiable")

    else:
        print("Starting the Local Development Environment")
        app.config.from_object(LocalDevelopmentConfig)
        upload_folder = app.config["UPLOAD_FOLDER"]
        print("Upload Folder: {}".format(upload_folder))
        
        db.init_app(app)
        

        app.app_context().push()
        return app
    

app = create_app()
#app.app_context().push()

from applications.controllers import *
app.run()

