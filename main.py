from flask import Flask, jsonify, request

app = Flask(__name__)

products_list = []
sales_list = []
purchases_list = []


@app.route("/", methods=["GET"]) 
def home():
    res = {"Flask API Version": "1.0"} 
    
    return jsonify(res), 200

@app.route("/api/products", methods=["GET","POST"])
def products():
    if request.method == "GET":
        return jsonify(products_list), 200
    elif request.method == "POST":
        data = request.get_json()
        if not data or "name" not in data or "buying_price" not in data or "selling_price" not in data:
            error = {"error": "Ensure all fields are set (name, buying_price, selling_price)"}
            return jsonify(error), 400
        else:
            products_list.append(data)
            return jsonify(data), 201
        
    else:
        error = {"error": "Method not allowed"} 
        return jsonify(error), 405  

if __name__ == "__main__":
    app.run(debug=True)
    

    
# Rest API HTTP rules
# 1. Have a route
# 3. Always return data as json
# 3. Specify the request method e.g. GET, POST
# 4. Return Status code

