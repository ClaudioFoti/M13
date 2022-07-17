from flask import Flask
import uuid

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"

@app.route("/host_id")
def host_id():
    host_id = str(uuid.uuid4())
    return host_id

@app.route("/health")
def health():
    return "I am alive", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)