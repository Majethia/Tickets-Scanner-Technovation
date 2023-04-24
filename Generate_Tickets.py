import pyqrcode
import sqlite3
import hashlib

connection = sqlite3.connect('db.sqlite3')
cur = connection.cursor()

def generate_qr(table, event):
    query = f"SELECT * FROM {table}"
    cur.execute(query)
    data = cur.fetchall()
    for i in data:
        id = i[0]
        hash = hashlib.md5(bytes(id))
        qr = pyqrcode.create(f"DSAII-{event.upper()}-ID-{id}-{hash.hexdigest()[:4]}")
        qr.png(f'{event.lower()}_qrs/{id}.png', scale = 8)

generate_qr("api_technovateam", "technova")
generate_qr("api_techathonteam", "techathon")
generate_qr("api_nerfarenateam", "nerfarena")
generate_qr("api_escaperoomteam", "escaperoom")
