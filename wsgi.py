import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect

# defaults to 'eventlet' gunicorn workers, if not specified otherwise in
# the GUNICORN_WORKER_CLASS env variable
# acceptable values: 'gevent', 'eventlet'
# todo, add value verification
async_mode = os.environ.get('GUNICORN_WORKER_CLASS', 'eventlet')

application = Flask(__name__)
application.config['SECRET_KEY'] = 'fsdjno342rfh094tn'
socketio = SocketIO(application, async_mpde=async_mode)

@application.route("/")
def hello():
    return "Hello World!"

@application.route("/ws")
def wsecho():
    return render_template("ws.html", async_mode=async_mode)

@socketio.on('my_event', namespace='/test')
def test_message(message):
    emit('my_response', {'data': message['data']})

@socketio.on('my_broadcast_event', namespace='/test')
def test_message(message):
    emit('my_response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected'})

@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    emit('my_response',  {'data': 'Disconnected!'})
    disconnect()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    #application.run()
    socketio.run(application)
