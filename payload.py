import json
import requests
from datetime import datetime, timedelta

url = "https://66f957adafc569e13a9882cf.mockapi.io/Payloads"
headers = {
    "Authorization": "66f957adafc569e13a9882cf",
    "Content-Type": "application/json"
}

class Payload:
    def payload(self, current_time, user_email, type, order_id):
        new_payload = {
            "order_id_buy": order_id,
            "datetime": current_time,
            "type": type
        }

        response = requests.get(url, headers=headers)
        users = response.json()
        
        user_data = next((user for user in users if user['user'] == user_email), None)

        if user_data:
            history = user_data.get('history', {})

            if 'paying' not in history:
                history['paying'] = []
            if 'payed' not in history:
                history['payed'] = []

            for payment in history['paying']:
                if payment['type'] == type:
                    data_time_str = payment['datetime']
                    data_time = datetime.strptime(data_time_str, '%Y-%m-%d %H:%M:%S')
                    if (datetime.now() - data_time) > timedelta(minutes=30):
                        history['payed'].append(payment)
                        history['paying'].remove(payment)
                        history['paying'].append(new_payload)
                        self._save_data(user_email, history)
                        return new_payload
                    else:
                        return history

            history['paying'].append(new_payload)
            self._save_data(user_email, history)
            return new_payload
        else:
            new_user = {
                "user": user_email,
                "status": "active",
                "history": {
                    "paying": [new_payload],
                    "payed": []
                }
            }
            self._save_data(user_email, new_user)
            return new_payload

    def _save_data(self, user_email, data):
        # Cập nhật dữ liệu vào API
        response = requests.put(f"{url}/{user_email}", headers=headers, json=data)
        if response.status_code == 404:  # Nếu không tìm thấy, tạo mới
            response = requests.post(url, headers=headers, json=data)
        if response.status_code not in [200, 201]:
            print(f"Error saving data: {response.text}")
