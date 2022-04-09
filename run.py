from threading import Thread
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from app import app
from app.babai import babai_app
from app.lwe import lwe_app

def babai_worker():
    server = Server({'/babai' : babai_app}, io_loop=IOLoop(), allow_websocket_origin=["*"], port=50007)
    server.start()
    server.io_loop.start()

def lwe_worker():
    server = Server({'/lwe' : lwe_app}, io_loop=IOLoop(), allow_websocket_origin=["*"], port=50008)
    server.start()
    server.io_loop.start()


Thread(target=babai_worker).start()
Thread(target=lwe_worker).start()


if __name__ == "__main__":
    #from waitress import serve #use this in production environment
    #serve(app, host="0.0.0.0", port=50000)
    app.run(debug=True, host="0.0.0.0", port=50000) #use this in dev environment