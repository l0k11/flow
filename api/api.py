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

@app.route("/api/messages/<string:id>", methods = ["GET", "POST"])
@cross_origin()
def messages(id):
    if request.method == "GET":
        my_id = os.environ["USER_ID"]
        other_id = id
        conv_id = other.client_get_conv_id(my_id, other_id, f"{pathlib.Path.home()}/.flow/.db", os.environ["SERVER_IP"])

        with sqlite3.connect(f"{pathlib.Path.home()}/.flow/.db") as con:
            select = con.execute("SELECT sender_id, receiver_id, content, time FROM messages WHERE conversation_id = ?", (conv_id,))
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
                other.execute_db_command(
                    f"{pathlib.Path.home()}/.flow/.db",
                    "INSERT INTO contacts VALUES (?,?)",
                    (id, name)
                )
                conv_id = other.client_get_conv_id(os.environ["USER_ID"], id, f"{pathlib.Path.home()}/.flow/.db", os.environ["SERVER_IP"])
                
                other.execute_db_command(
                    f"{pathlib.Path.home()}/.flow/.db",
                    "UPDATE conversations SET name = ? WHERE id = ?",
                    (name, conv_id)
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
            conv_id = other.client_get_conv_id(os.environ["USER_ID"], id, f"{pathlib.Path.home()}/.flow/.db", os.environ["SERVER_IP"])
            other.execute_db_command(
                f"{pathlib.Path.home()}/.flow/.db",
                "UPDATE conversations SET name = ? WHERE id = ?",
                (name, conv_id)
            )
            return jsonify({"status": "0"})
        else: return jsonify({"status": "1"})

    elif request.method == "DELETE":
        id = request.json["id"]
        ip = con.get_ip(id, os.environ["SERVER_IP"])
        conv_id = other.client_get_conv_id(os.environ["USER_ID"], id, f"{pathlib.Path.home()}/.flow/.db", os.environ["SERVER_IP"])
        print(f"Cambiando nombre a {ip}")
        other.execute_db_command(
            f"{pathlib.Path.home()}/.flow/.db",
            "UPDATE conversations SET name = ? WHERE id = ?",
            (ip, conv_id)
        )
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
            "SELECT id, name, lastMsg, lastMsgTime FROM conversations ORDER BY lastMsgTime DESC"
        )
        result = select.fetchall()
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