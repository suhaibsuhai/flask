from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    cert_path = os.path.join(os.path.dirname(__file__), 'cert.pem')
    key_path = os.path.join(os.path.dirname(__file__), 'privkey.pem')
    
    app.run(host='0.0.0.0', port='8080', ssl_context=(cert_path, key_path))
