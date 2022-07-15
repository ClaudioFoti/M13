from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"

@app.route("/host_id")
def host_id():
    return "UUID"

@app.route("/health")
def health():
    return "health"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)