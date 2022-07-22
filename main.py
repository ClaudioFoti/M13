from flask import Flask
import uuid
import mysql.connector
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"

@app.route("/host_id")
def host_id():
    name = os.environ['NAME']
    
    db = mysql.connector.connect(
        host="db",
        user="root",
        password="",
        database="module13"
    )

    cursor = db.cursor()
    cursor.execute("SELECT host_id FROM hosts where name = '"+ name +"'")
    result = cursor.fetchone()

    host_id = str(result[0])
    return host_id

@app.route("/health")
def health():
    return "I am alive", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)