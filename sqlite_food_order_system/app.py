from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder='static')
DB_PATH = 'database.db'

def init_db():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            with open('schema.sql', 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        print("✅ 資料庫已初始化")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route('/api/orders', methods=['POST'])
def save_orders():
    data = request.get_json()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for item in data:
        cursor.execute('''
            INSERT INTO orders (product, quantity, price, subtotal)
            VALUES (?, ?, ?, ?)
        ''', (item['product'], item['quantity'], item['price'], item['subtotal']))

    conn.commit()
    conn.close()
    return jsonify({'message': '成功儲存訂單！'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=3000)