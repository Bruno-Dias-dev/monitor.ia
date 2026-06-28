import mysql.connector

db = mysql.connector.connect(
    host="easypanel.lum3.com.br",
    port=3006,
    user="root",
    password="Hb181020",
    database="monitor_ia"
)

print("Conectou!")