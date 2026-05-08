<<<<<<< HEAD
from flask import Flask

app = Flask(__name__)
env = app.config.get("ENV", "development")

if env == "production":
    app.config.from_object("config.ProductionConfig")
elif env == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

=======
from flask import Flask

app = Flask(__name__)
env = app.config.get("ENV", "development")

if env == "production":
    app.config.from_object("config.ProductionConfig")
elif env == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

>>>>>>> aac06878b7a1a810ea638f269f262f646de801d0
from app import views