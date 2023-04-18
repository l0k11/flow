import socket, sqlite3, uuid, os
from time import time

def get_private_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    private_ip = s.getsockname()[0]
    s.close()
    return private_ip

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def execute_db_command(db, command, args : tuple = None):
    with sqlite3.connect(db) as con:
        try: 
            command = con.execute(command, args) if args else con.execute(command)
            return command
        except Exception as e:
            con.close()
            raise e
        
def get_conv_id(idSender, idReceiver, db):
    with sqlite3.connect(db) as con:
        try:
            name = f"{idSender},{idReceiver}"
            select = con.execute("SELECT id FROM conversations WHERE users = ?", (name,))
            result = select.fetchall()
            if len(result): return result[0][0]
            else:
                name = f"{idReceiver},{idSender}"
                select = con.execute("SELECT id FROM conversations WHERE users = ?", (name,))
                result = select.fetchall()
                if len(result): return result[0][0]
                else:
                    while True:
                        id = f"c{uuid.uuid4()}"
                        select = con.execute("SELECT id FROM conversations WHERE id = ?", (id,))
                        result = select.fetchall()

                        if not len(result):
                            con.execute("INSERT INTO conversations VALUES (?,?)", (id, name))
                            return id
        except Exception as e:
            con.close()
            raise e