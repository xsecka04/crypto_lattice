from flask import Flask
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

app = Flask(__name__)

bootstrap.init_app(app)

from . import babai
from . import lwe_basis
from . import algorithm
from . import views
