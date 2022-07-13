from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"

@app.route("/host_id")
def host_id():
    print(vars(request.headers))
    return "UUID"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
