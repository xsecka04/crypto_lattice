from threading import Thread
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from app import app
from app.babai import babai_app

def bk_worker():
    server = Server({'/babai' : babai_app}, io_loop=IOLoop(), allow_websocket_origin=["*"], port=50007)
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()

if __name__ == "__main__":
    from waitress import serve #use this in production environment
    serve(app, host="0.0.0.0", port=50000)
    #app.run(debug=True, host="0.0.0.0", port=50000) #use this in dev environment