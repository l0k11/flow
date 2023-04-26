from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import re, pathlib, sqlite3, uuid, os,\
    functions.other as other, functions.conection as con

load_dotenv(f"{pathlib.Path.home()}/.flow/.env")

app = Flask(__name__)
socket = SocketIO(app)
CORS(app)

@app.route("/")
@cross_origin()
def root():
    # <script src="{{ url_for('static', filename='js/script.js') }}"></script>
    return render_template("hola.html")

@app.route("/api/messages/<string:idContact>", methods = ["GET", "POST"])
@cross_origin()
def messages(idContact):
    idPattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$"

    # if re.search(idPattern, idMain) and re.search(idPattern, idContact):
    #     conv_id = other.get_conv_id(idMain, idContact, f"{root}.db")
    if request.method == "GET":
        with sqlite3.connect(f"{pathlib.Path.home()}/.flow/.db") as con:
            # select = con.execute("SELECT * FROM messages WHERE conversation_id = ?", (conv_id,))
            select = con.execute("SELECT * FROM contacts")
            result = select.fetchall()
    return jsonify(result)

@app.route("/api/my-id", methods = ["GET"])
@cross_origin()
def my_id():
    return jsonify({"id": os.environ["USER_ID"]})

@app.route("/api/contacts", methods=["GET", "POST"])
@cross_origin()
def contacts():
    if request.method == "GET":
        select = other.execute_db_command(
            f"{pathlib.Path.home()}/.flow/.db",
            "SELECT * FROM contacts"
        )
        result = select.fetchall()
        del result[0]
        return jsonify(result)
    
    elif request.method == "POST":
        try:
            name = request.json["name"]
            ip = request.json["ip"]
            con.check_ip()

        except Exception as e:
            raise e


@app.route("/adri/<string:loquesea>")
def loquesea(loquesea):
    return jsonify({"hola": loquesea})


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