from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import re, pathlib, sqlite3, uuid, functions.other as other

# <script src="{{ url_for('static', filename='js/script.js') }}"></script>

app = Flask(__name__)
socket = SocketIO(app)
CORS(app)

@app.route("/")
@cross_origin()
def root():
    return render_template("hola.html")

@app.route("/api/user/<string:idMain>/messages/<string:idContact>", methods = ["GET", "POST"])
@cross_origin()
def messages(idMain, idContact):
    idPattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"
    root = f"{pathlib.Path.home()}/.flow/"

    # if re.search(idPattern, idMain) and re.search(idPattern, idContact):
    #     conv_id = other.get_conv_id(idMain, idContact, f"{root}.db")
    if request.method == "GET":
        with sqlite3.connect(f"{root}.db") as con:
            # select = con.execute("SELECT * FROM messages WHERE conversation_id = ?", (conv_id,))
            select = con.execute("SELECT * FROM contacts")
            result = select.fetchall()
    return jsonify(result)


@app.route("/api/my-id", methods = ["GET"])
 
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