import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    with open('schema.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()
    print("資料庫初始化完成！")

if __name__ == '__main__':
    init_db()
