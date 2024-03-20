import os
from flask import Flask, request, jsonify
import diarise
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Accepts POST requests at /webhook endpoint
@app.route('/dir', methods=['POST'])
def index():
    id=request.json['ID']
    date=request.json['date']
    time=request.json['time']
    r=diarise.start(date,time)
    return ({"result":r})


if __name__=="__main__":
    app.run(debug=True,port=6000)

