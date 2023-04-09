from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socket = SocketIO(app)

@app.route("/")
def root():
    return render_template("hola.html")

@app.route("/json")
def json():
    return jsonify({
        'hola': 'que tal estas'
    })
 
@socket.on('connect')
def handle_connect():
    print('Client connected')

@socket.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socket.on("my event")
def handle_event(data):
    print(f'Client here: {data}')

socket.run(app)