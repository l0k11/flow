from flask import Flask, render_template, jsonify, request, make_response, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import pathlib, sqlite3, os, time,\
    functions.other as other, functions.conection as conection

load_dotenv(f"{pathlib.Path.home()}/.flow/.env")

app = Flask(__name__, static_folder='web/build')
socket = SocketIO(app)
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin()
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route("/api/messages/<string:id>", methods = ["GET", "POST"])
@cross_origin()
def messages(id):
    my_id = os.environ["USER_ID"]
    other_id = id
    conv_id = other.client_get_conv_id(my_id, other_id, f"{pathlib.Path.home()}/.flow/.db", os.environ["SERVER_IP"])

    if request.method == "GET":
        with sqlite3.connect(f"{pathlib.Path.home()}/.flow/.db") as con:
            select = con.execute("SELECT sender_id, receiver_id, content, time FROM messages WHERE conversation_id = ? ORDER BY time DESC", (conv_id,))
            result = select.fetchall()
        return jsonify(result)

    elif request.method == "POST":
        content = request.json["content"]
        MSGTime = request.json["time"]
        MSGID = conection.generate_id(os.environ["SERVER_IP"], "message")
        conv_id = other.client_get_conv_id(my_id, other_id, f"{pathlib.Path.home()}/.flow/.db", os.environ["SERVER_IP"])
        other.execute_db_command(
            f"{pathlib.Path.home()}/.flow/.db",
            "INSERT INTO messages VALUES (?,?,?,?,?,?)",
            (MSGID, conv_id, my_id, other_id, content, MSGTime)   
        )
        conection.send_message(
            ip = os.environ["SERVER_IP"],
            port = 6002,
            idMessage = MSGID,
            idSender = my_id,
            idReceiver = other_id,
            content = content,
            MTime = MSGTime,
            key_file = f"{pathlib.Path.home()}/.flow/server.key"
        )
        return jsonify({"status": "0"})

@app.route("/api/my-id", methods = ["GET"])
@cross_origin()
def my_id():
    return jsonify({"id": os.environ["USER_ID"]})

@app.route("/api/contacts", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
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
        id = conection.check_ip(os.environ["SERVER_IP"], ip)
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

    elif request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "DELETE")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        return response

    elif request.method == "DELETE" or request.method == "OPTIONS":
        id = request.json["id"]
        print(os.environ["SERVER_IP"])
        ip = conection.get_ip(id, os.environ["SERVER_IP"])
        conv_id = other.client_get_conv_id(os.environ["USER_ID"], id, f"{pathlib.Path.home()}/.flow/.db", os.environ["SERVER_IP"])
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
            "SELECT * FROM conversations ORDER BY lastMsgTime DESC"
        )
        result = select.fetchall()
        return jsonify(result)

if __name__ == "__main__":
    socket.run(app)