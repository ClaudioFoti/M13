from flask import Flask,redirect,request
import requests
import os
import datetime
import boto3
import botocore

CONFIG_FILE = "config_files/config.csv"
DEFAULT_SERVER_POOL = [("127.0.0.1",8081),("127.0.0.1",8082),("127.0.0.1",8083)]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
bucket = s3.Bucket('module13-hosts-config')

@app.route("/")
def index():
    return redirect_to_fastest("/")

@app.route("/host_id")
def host_id():
    return redirect_to_fastest("/host_id")

@app.route("/health")
def health():
    return redirect_to_fastest("/health")

@app.route('/hosts_configuration', methods=['GET', 'POST'])
def upload_file():
    response = ""
    if request.method == 'POST':
        if 'file' not in request.files:
            response += "No file part"
        else:
            file = request.files['file']
            response += upload_file_to_bucket(file,bucket)

    if request.method == 'GET':
        response += get_latest_config_file(bucket)

    return '''
    <!doctype html>
    <title>Upload config File for hosts</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''+response

def allowed_file(filename):
    allowed_extensions = ['csv']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_latest_config_file(bucket):
    objects = s3_client.list_objects_v2(Bucket=bucket.name)["Contents"]
    latest = max(objects, key=lambda x: x['LastModified'])['Key']

    try:
        s3.Bucket(bucket.name).download_file(latest, 'config_files/config.csv')

        return "Latest config file acquired"
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return "The object does not exist"
        else:
            return "Config file couldn't be downloaded"

def get_server_pool():
    server_pool = []

    if os.path.isfile(CONFIG_FILE):
        file = open(CONFIG_FILE, "r")
        file.readline()
        for row in file:
            port = row.split(';')[2]
            server_pool.append(("127.0.0.1",port))

    return server_pool

def upload_file_to_bucket(file, bucket):
    if file.filename == '':
        return "No file uploaded"
    if file and allowed_file(file.filename):
        extenstion = file.filename.split('.')[1]

        filename = "config_" + str(datetime.datetime.now()).replace(":", "_").split('.')[0] + "." + extenstion
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(filepath)
        data = open(filepath, 'rb')

        bucket.put_object(Key=filename, Body=data)

        get_latest_config_file(bucket)
        
        return "File successfully uploaded"

    return "File couldn't be uploaded"

def get_fastest_server():
    server_pool = get_server_pool()

    if not server_pool:
        server_pool = DEFAULT_SERVER_POOL

    fastest_server = server_pool[0]
    fastest_time = 1
    for server in server_pool:
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
    get_latest_config_file(bucket)
    app.run(host="0.0.0.0", port=8080, debug=True)