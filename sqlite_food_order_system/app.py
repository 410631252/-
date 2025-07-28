from flask import Flask, request, jsonify, render_template, send_from_directory
from pymongo import MongoClient
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(24)

# MongoDB 連接
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["food_order_system"]
    menu_collection = db["menu"]
    orders_collection = db["orders"]
    print(" MongoDB 連接成功")
except Exception as e:
    print(f" MongoDB 連接失敗: {str(e)}")
    raise

def init_menu_data():
    try:
        if menu_collection.count_documents({}) == 0:
            with open("data.json", "r", encoding="utf-8") as f:
                menu_data = json.load(f)
                menu_collection.insert_one(menu_data)
                print(" 菜單資料初始化成功")
    except Exception as e:
        print(f" 菜單初始化失敗: {str(e)}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/menu")
def get_menu():
    try:
        menu_doc = menu_collection.find_one()
        if menu_doc and "menu" in menu_doc:
            return jsonify({"menu": menu_doc["menu"]})
        return jsonify({"menu": {}})
    except Exception as e:
        print(f"獲取菜單錯誤: {str(e)}")
        return jsonify({"error": "無法獲取菜單"}), 500

@app.route("/api/orders", methods=["GET", "POST"])
def handle_orders():
    if request.method == "POST":
        try:
            data = request.json
            customer_name = data.get("customer_name")
            items = data.get("items", [])
            
            if not customer_name or not items:
                return jsonify({"error": "缺少必要資訊"}), 400

            new_order = {
                "customer_name": customer_name,
                "items": items,
                "order_time": datetime.now().isoformat(),
                "status": "pending",
                "total_price": sum(item.get("price", 0) * item.get("quantity", 0) for item in items)
            }
            
            result = orders_collection.insert_one(new_order)
            
            return jsonify({
                "message": "訂單已成功建立",
                "order_id": str(result.inserted_id)
            })
            
        except Exception as e:
            print(f"建立訂單錯誤: {str(e)}")
            return jsonify({"error": "建立訂單失敗"}), 500
    
    else:
        try:
            orders = list(orders_collection.find())
            for order in orders:
                order["_id"] = str(order["_id"])
            return jsonify({"orders": orders})
        except Exception as e:
            print(f"獲取訂單錯誤: {str(e)}")
            return jsonify({"error": "獲取訂單失敗"}), 500

if __name__ == "__main__":
    init_menu_data()
    print("\n系統已啟動！")
    print("請訪問：http://localhost:3000")
    app.run(debug=True, port=3000)
