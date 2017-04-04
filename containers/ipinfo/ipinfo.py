import os
from flask import Flask, redirect, url_for, render_template, request
import json
import requests

app = Flask(__name__)

client = MongoClient(os.environ['DB_1_PORT_27017_TCP_ADDR'], 27017)
db= client.db

@app.route('/')
def help():
    help = "Format for accessing. 'https://ipAddress/ipinfo/url_to_search' But anyway You made it here"
    return help
@app.route('/ipinfo')
@app.route('/ipinfo/<ip>')
def ipinfo(ip=''):
    lookup = "http://ipinfo.io/" + ip
    result = requests.get(lookup)
    insertionResult = insertRecord(json.loads(result.text))
    if (insertionResult['status'] != "Success"):
        return insertionResult
    insertionResult['result'] = result.text
    return insertionResult

def insertRecord(record):
    try:
        id = db.ipinfo.insert_one(record).inserted_id
        return {"status":"Success", "id":id}
    except Exception as e:
        return {"status":"Failure", "error": str(e)}
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5002, debug=True)

