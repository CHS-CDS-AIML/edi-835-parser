from flask import Flask, request
#import requests
import base64
import os

app = Flask(__name__)

@app.route("/show_project", methods=['POST', 'GET'])
def print_project():
    print(f"PROJECT IS {os.getenv('PROJECT')}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
