from flask import Flask,redirect
import requests

SERVER_POOL = [('127.0.0.1',8081),('127.0.0.1',8082),('127.0.0.1',8083)]

app = Flask(__name__)

@app.route("/")
def index():
    return redirect_to_fastest("/")

@app.route("/host_id")
def host_id():
    return redirect_to_fastest("/host_id")

@app.route("/health")
def health():
    return redirect_to_fastest("/health")

def get_fastest_server():
    fastest_server = SERVER_POOL[0]
    fastest_time = 1
    for server in SERVER_POOL:
        url = "http://"+server[0]+":"+str(server[1])+"/health"
        try:
            response = requests.get(url, timeout=fastest_time)
        except:
            response.status_code = 503
        if response.status_code == 200:
            time = response.elapsed.total_seconds()
            if time < fastest_time:
                fastest_time = time
                fastest_server = server
    
    return fastest_server

def redirect_to_fastest(route):
    server = get_fastest_server()
    url = "http://"+server[0]+":"+str(server[1])+route
    return redirect(url,code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)