from flask import Flask, jsonify, request

app = Flask(__name__)

products_list = []
sales_list = []
purchases_list = []

def is_int(value):
    try:
        int(value)
        return True
    except(ValueError, TypeError):
        return False
    
def is_number():
    try:
        float(value)
        return(True)
    except(ValueError, TypeError):
        return False
        

@app.route("/", methods=["GET"]) 
def home():
    res = {"Flask API Version": "1.0"} 
    
    return jsonify(res), 200

@app.route("/api/products", methods=["GET","POST"])
def products():
    if request.method == "GET":
        return jsonify(products_list), 200
    elif request.method == "POST":
        data = dict(request.get_json())
        if not data or "name" not in data or "buying_price" not in data or "selling_price" not in data:
            error = {"error": "Ensure all fields are set (name, buying_price, selling_price)"}
            return jsonify(error), 400
        else:
            products_list.append(data)
            return jsonify(data), 201
        
    else:
        error = {"error": "Method not allowed"} 
        return jsonify(error), 405  
    
@app.route("/api/sales", methods=["GET", "POST"])
def sales():
    if request.method == "GET":
        return jsonify(sales_list), 200
    
    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request must be in json"}), 400
        
        if "product_id" not in data or "quantity" not in data:
            return jsonify({"error": "Ensure all fields are set: product_id, quantity"}), 400
        
@app.route("/api/purchases", methods=["GET", "POST"])
def purchases():
    if request.method == "GET":
        return jsonify(purchases_list), 200
    
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"Error": "Request must be in JSON"}), 400
            if "product_id" not in data or "quantity" not in data:
                return jsonify({"error": "Ensure all fields are set: product_id, quantity"}), 400
            elif is_int(data[product_id]):
                return jsonify({"error":"product_id must be an int"}), 400
            if not is_number(data["quantity"]):
                return jsonify({"error":"Quantity Must be a number"}), 400
            else:
                purchase = {
                    "product_id": int(data["product_id"]),
                    "quantity": float(data["quantity"]),
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            purchases_list.append(purchase)
            return jsonify(purchase), 201
        else:
            return jsonify({"error": "Method not allowed"}), 405
        

if __name__ == "__main__":
    app.run(debug=True)
    

    
# Rest API HTTP rules
# 1. Have a route
# 3. Always return data as json
# 3. Specify the request method e.g. GET, POST
# 4. Return Status code

