from bokeh.embed import server_document
from flask import render_template
from . import app
import os

#ip = os.environ.get('IP')

@app.route('/', methods=['GET'])
def babai_page():
    #script = server_document(f'http://{ip}:50007/babai')
    script = server_document(f'http://localhost:50007/babai')
    return render_template("index.html", script=script, template="Flask")



#@app.route('/lwe', methods=['GET'])
#def lwe_page():
#    #script = server_document(f'http://{ip}:50007/babai')
#    script = server_document(f'http://localhost:50008/lwe')
#    return render_template("index.html", script=script, template="Flask")


@app.route('/alg', methods=['GET'])
def lwe_page():
    #script = server_document(f'http://{ip}:50007/babai')
    script = server_document(f'http://localhost:50010/alg')
    return render_template("index.html", script=script, template="Flask")
