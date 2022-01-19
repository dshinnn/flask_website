from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'try to guess me'

from . import routes