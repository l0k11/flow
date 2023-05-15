import sqlite3, pathlib, uuid
conv_id = "ce8e5351f-6ed7-40d5-be39-6f8f058a8b08"
my_id = "u37c64162-f8c1-4985-ae09-d67ef858c571"
other_id = "u1bb37dff-c60e-4f29-977f-28a63015b4a6"
with sqlite3.connect(f"{pathlib.Path.home()}/.flow/.db") as con:
    con.execute("INSERT INTO messages VALUES (?,?,?,?,?,?)",
        (f"m{uuid.uuid4()}", conv_id, my_id, other_id, "1", "1683739411"))
    con.execute("INSERT INTO messages VALUES (?,?,?,?,?,?)",
        (f"m{uuid.uuid4()}", conv_id, my_id, other_id, "2", "1683559411"))
    con.execute("INSERT INTO messages VALUES (?,?,?,?,?,?)",
        (f"m{uuid.uuid4()}", conv_id, my_id, other_id, "3", "1683645811"))
    con.execute("INSERT INTO messages VALUES (?,?,?,?,?,?)",
        (f"m{uuid.uuid4()}", conv_id, my_id, other_id, "4", "1680801566"))
    con.execute("INSERT INTO messages VALUES (?,?,?,?,?,?)",
        (f"m{uuid.uuid4()}", conv_id, my_id, other_id, "5", "1683739411"))
    con.execute("INSERT INTO messages VALUES (?,?,?,?,?,?)",
        (f"m{uuid.uuid4()}", conv_id, my_id, other_id, "6", "1683739411"))    