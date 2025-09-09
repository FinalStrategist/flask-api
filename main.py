from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"]) 
def home():
    res = {"Flask API Version": "1.0"} 
    
    return jsonify(res), 200

if __name__ == "__main__":
    app.run(debug=True)  