import threading, sqlite3, schedule, time

# Este es el servicio que se encarga de comprobar desconexiones de los clientes, lo hace cada 5 minutos
# y funciona haciendo que, a partir de una hora que hay en la base de datos que se actualiza en cada conexión de control,
# este código comprueba si la conexión fue hace más de 3 minutos. Si lo es, marca el contacto como desconectado y 
# así el servidor evita muchos envíos innecesarios de paquetes.

class CheckStatus(threading.Thread):
    def __init__(self, db_file):
        threading.Thread.__init__(self)
        self.db = db_file

    def run(self):
        schedule.every(5).minutes.do(self.check_status)

        while True:
            schedule.run_pending()
            time.sleep(10)

    def check_status(self):
        with sqlite3.connect(self.db) as con:
            try:
                select = con.execute("SELECT id, lastCheck FROM users WHERE status = 'online'")
                result = select.fetchall()
                min3 = int(round(time.time() * 1000)) - 180000
                for row in result:
                    if row[1] < min3:
                        con.execute("UPDATE users SET status = 'disconnected' WHERE id = ?", (row[0],))

            except Exception as e:
                con.close()
                raise e