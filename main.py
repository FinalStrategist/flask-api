from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import datetime 

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "MyApi123"
jwt = JWTManager(app)
products_list = []
sales_list = []
purchases_list = []
users_list = []

def is_int(value):
    try:
        int(value)
        return True
    except(ValueError, TypeError):
        return False
    
def is_number(value):
    try:
        float(value)
        return True
    except(ValueError, TypeError):
        return False

@app.route("/", methods=["GET"]) 
def home():
    res = {"Flask API Version": "1.0"} 
    
    return jsonify(res), 200

@app.route("/api/users", methods=["GET"])
def users():
    return jsonify(users_list), 200

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data or "password" not in data:
        error = {"error": "Ensure all fields are set"}
        return jsonify(error), 400
    else:
        users_list.append(data)
        # Create a token
        token = create_access_token(identity=data["email"])
        return jsonify({"user": data, "token": token}), 201  
    
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        error = {"error": "Make sure all fields are set"}
        return jsonify(error), 400
    else:
        for u in users_list:
            if u["email"] == data["email"] and u["password"] == data["password"]:
                # return a token
                token = create_access_token(identity=data["email"])
                return jsonify({"message": "Login successful", "token": token}), 200
        return jsonify({"message": "Incorrect credentials"}), 401

@app.route("/api/products", methods=["GET","POST"])
@jwt_required
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
        
        if not is_int(data["product_id"]):
            return jsonify({"error": "product_id must be an integer"}), 400
        if not is_number(data["quantity"]):
            return jsonify({"error": "Quantity must be a number"}), 400
            
        sale = {
            "product_id": int(data["product_id"]),
            "quantity": float(data["quantity"]),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        sales_list.append(sale)
        return jsonify(sale), 201
    
    else:
        return jsonify({"error": "Method not allowed"}), 405

@app.route("/api/purchases", methods=["GET", "POST"])
def purchases():
    if request.method == "GET":
        return jsonify(purchases_list), 200
    
    elif request.method == "POST": 
        data = request.get_json()
        if not data:
            return jsonify({"Error": "Request must be in JSON"}), 400
        
        if "product_id" not in data or "quantity" not in data:
            return jsonify({"error": "Ensure all fields are set: product_id, quantity"}), 400
        elif not is_int(data["product_id"]):
            return jsonify({"error": "product_id must be an integer"}), 400
        if not is_number(data["quantity"]):
            return jsonify({"error": "Quantity must be a number"}), 400
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

# JWT
# Is a JSON Web Tokens generated in the api and sent to the client.
# A client (Web, Mobile) cannot access a protected route without a token.
# The client stores  that token once it is generated and sends it with a request  e.g /products
# The token is usually added in the header part of the request.

