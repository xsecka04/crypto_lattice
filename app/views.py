from bokeh.embed import server_document
from flask import render_template
from . import app

@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/babai')
    return render_template("index.html", script=script, template="Flask")
