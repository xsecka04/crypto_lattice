from threading import Thread
from bokeh.server.server import Server
from flask import request
from tornado.ioloop import IOLoop
from app import app
from app.babai import babai_app

def bk_worker():
    #server = Server({'/babai' : babai_app}, io_loop=IOLoop(), allow_websocket_origin=['localhost:8000', '127.0.0.1:8000'])
    server = Server({'/babai' : babai_app}, io_loop=IOLoop(), allow_websocket_origin=['0.0.0.0:50000'], port=50007)
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=50000)