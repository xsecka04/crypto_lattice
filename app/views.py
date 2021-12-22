from bokeh.embed import server_document
from flask import render_template
from . import app
import os

#ip = os.environ.get('IP')

@app.route('/', methods=['GET'])
def bkapp_page():
    #script = server_document(f'http://{ip}:50007/babai')
    script = server_document(f'http://localhost:50007/babai')
    return render_template("index.html", script=script, template="Flask")
