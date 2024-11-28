from flask import Flask, request
import base64
import os
from edi_835_parser.parse_835 import parse_daily_files

app = Flask(__name__)

@app.route("/show_project", methods=['POST', 'GET'])
def print_project():
    print(f"PROJECT IS {os.getenv('PROJECT')}")

@app.route("/parse_files", methods=['POST'])
def parse_files():
    parse_daily_files()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
