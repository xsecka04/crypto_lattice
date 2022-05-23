from threading import Thread
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
from app import app
from app.babai import babai_app
from app.algorithm import alg_app
from app.lwe_basis import lwe_basis_app


#from app.lwe import lwe_app

def app_worker():
    server = Server({'/babai' : babai_app, '/alg' : alg_app, '/lwe_basis' : lwe_basis_app}, io_loop=IOLoop(), allow_websocket_origin=["*"], port=50007)
    server.start()
    server.io_loop.start()

#def alg_worker():
#    server = Server({'/alg' : alg_app}, io_loop=IOLoop(), allow_websocket_origin=["*"], port=50010)
#    server.start()
#    server.io_loop.start()

#def lwe_basis_app_worker():
#    server = Server({'/lwe_basis' : lwe_basis_app}, io_loop=IOLoop(), allow_websocket_origin=["*"], port=50011)
#    server.start()
#    server.io_loop.start()


Thread(target=app_worker).start()
#Thread(target=lwe_worker).start()
#Thread(target=alg_worker).start()
#Thread(target=lwe_basis_app_worker).start()



if __name__ == "__main__":
    #from waitress import serve #use this in production environment
    #serve(app, host="0.0.0.0", port=50000)
    app.run(debug=True, host="localhost", port=50000) #use this in dev environment