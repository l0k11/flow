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

@app.route("/api/contacts", methods=["GET", "POST", "PUT", "DELETE"])
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
        name = request.json["name"]
        ip = request.json["ip"]
        id = con.check_ip(os.environ["SERVER_IP"], ip)
        if id != "0":
            select = other.execute_db_command(
                f"{pathlib.Path.home()}/.flow/.db",
                "SELECT * FROM contacts WHERE id = ?",
                (id,)
            )
            result = select.fetchall()
            if result: return jsonify({"status": "1"})
            else:
                conv_id = other.client_get_conv_id(os.environ["USER_ID"], id, f"{pathlib.Path.home()}/.flow/.db", os.environ["SERVER_IP"])
                select = other.execute_db_command(
                    f"{pathlib.Path.home()}/.flow/.db",
                    "SELECT content, time FROM messages WHERE conversation_id = ? ORDER BY time DESC LIMIT 1",
                    (conv_id,)
                )
                result = select.fetchall()
                last_msg = result[0] if result else [None, None]
                
                other.execute_db_command(
                    f"{pathlib.Path.home()}/.flow/.db",
                    "INSERT INTO contacts VALUES (?,?)",
                    (id, name)
                )
                return jsonify({"status": "0"})
        else: return jsonify({"status": "2"})

    elif request.method == "PUT":
        name = request.json["name"]
        id = request.json["id"]
        check = other.execute_db_command(
            f"{pathlib.Path.home()}/.flow/.db",
            "SELECT id FROM contacts WHERE name = ?",
            (name,)
        )
        resultCheck = check.fetchall()
        if not resultCheck:
            other.execute_db_command(
                f"{pathlib.Path.home()}/.flow/.db",
                "UPDATE contacts SET name = ? WHERE id = ?",
                (name, id)
            )
            convID = other.client_get_conv_id(os.environ["USER_ID"], id)
            other.execute_db_command(
                f"{pathlib.Path.home()}/.flow/.db",
                "UPDATE conversations SET name = ? WHERE id = ?",
                (os.environ["USER_ID"], convID)
            )
            return jsonify({"status": "0"})
        else: return jsonify({"status": "1"})

    elif request.method == "DELETE":
        id = request.json["id"]
        other.execute_db_command(
            f"{pathlib.Path.home()}/.flow/.db",
            "DELETE FROM contacts WHERE id = ?",
            (id,)
        )
        return jsonify({"status": "0"})


@app.route("/api/convs", methods=["GET", "POST", "DELETE"])
@cross_origin()
def convs():
    if request.method == "GET":
        select = other.execute_db_command(
            f"{pathlib.Path.home()}/.flow/.db",
            "SELECT * FROM conversations"
        )
        result = select.fetchall()
        del result[0]
        return jsonify(result)

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