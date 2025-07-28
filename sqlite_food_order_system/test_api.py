import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:3000'

def test_register():
    print('1. 測試註冊新使用者...')
    register_data = {
        'email': f'test_{datetime.now().strftime("%Y%m%d%H%M%S")}@example.com',
        'password': 'test123',
        'name': '測試使用者'
    }
    response = requests.post(f'{BASE_URL}/api/users/register', json=register_data)
    print(f'註冊結果: {response.status_code}')
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    return response.cookies

def test_login():
    print('\n2. 測試登入...')
    login_data = {
        'email': 'test@example.com',
        'password': 'test123'
    }
    response = requests.post(f'{BASE_URL}/api/users/login', json=login_data)
    print(f'登入結果: {response.status_code}')
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    return response.cookies

def test_create_order(cookies):
    print('\n3. 測試建立訂單...')
    order_data = {
        'customer_name': '測試使用者',
        'items': [
            {
                'product_id': 1,  # 紅燒牛肉麵
                'quantity': 2
            },
            {
                'product_id': 7,  # 珍珠奶茶
                'quantity': 1
            }
        ]
    }
    response = requests.post(f'{BASE_URL}/api/orders', json=order_data, cookies=cookies)
    print(f'訂單結果: {response.status_code}')
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

def test_get_orders(cookies):
    print('\n4. 測試獲取訂單列表...')
    response = requests.get(f'{BASE_URL}/api/orders', cookies=cookies)
    print(f'訂單列表結果: {response.status_code}')
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

def test_get_menu():
    print('\n5. 測試獲取菜單...')
    response = requests.get(f'{BASE_URL}/api/menu')
    print(f'菜單結果: {response.status_code}')
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

def test_get_profile(cookies):
    print('\n6. 測試獲取使用者資料...')
    response = requests.get(f'{BASE_URL}/api/users/profile', cookies=cookies)
    print(f'使用者資料結果: {response.status_code}')
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    print('開始 API 測試...\n')
    
    # 執行註冊測試
    cookies = test_register()
    
    # 執行登入測試
    cookies = test_login()
    
    # 測試獲取菜單
    test_get_menu()
    
    # 執行訂單相關測試
    test_create_order(cookies)
    test_get_orders(cookies)
    
    # 測試使用者資料
    test_get_profile(cookies)
    
    print('\n測試完成！')
