from bokeh.embed import server_document
from flask import jsonify, render_template
from . import app
import os

ip = os.environ.get('IP')
#ip = "localhost" #use in case of venv deployment

@app.route('/', methods=['GET'])
def babai_page():
    script = server_document(f'http://{ip}:50007/babai')
    return render_template("index.html", script=script, template="Flask")

@app.route('/alg', methods=['GET'])
def alg_page():
    script = server_document(f'http://{ip}:50007/alg')
    return render_template("alg.html", script=script, template="Flask")


@app.route('/lwe_basis', methods=['GET'])
def lwe_basis_page():
    script = server_document(f'http://{ip}:50007/lwe_basis')
    return render_template("lwe.html", script=script, template="Flask")



