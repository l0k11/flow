import socket, sqlite3, uuid, os, functions.conection as conection

# Aquí almaceno funciones varias que he usado en muchos sitios pero que no tenían una
# categoria específica 

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
            select = con.execute(command, args) if args else con.execute(command)
            return select
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
        
def client_get_conv_id(idSender, idReceiver, db, ip):
    with sqlite3.connect(db) as con:
        try:
            users = f"{idSender},{idReceiver}"
            select = con.execute("SELECT id FROM conversations WHERE users = ?", (users,))
            result = select.fetchall()
            if len(result): return result[0][0]
            else:
                users = f"{idReceiver},{idSender}"
                select = con.execute("SELECT id FROM conversations WHERE users = ?", (users,))
                result = select.fetchall()
                if len(result): return result[0][0]
                else:
                    id = conection.generate_id(ip, "conversation")
                    con.execute("INSERT INTO conversations VALUES (?,?,?)", (id, users, None))
                    return id
                    
        except Exception as e:
            con.close()
            raise e