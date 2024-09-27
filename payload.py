import json
from datetime import datetime, timedelta

class Payload:
    def __init__(self) -> None:
        # Đọc file JSON
        with open('data/payloads.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    def payload(self, current_time, user_email, type, order_id):
        # Tạo payload mới
        new_payload = {
            "order_id_buy": order_id,
            "datetime": current_time,
            "type": type
        }
        user_found = False
        for user_data in self.data['data']:
            if user_data['user'] == user_email:
                user_found = True
                history = user_data['history']
                for payment in history['paying']:
                    if payment['type'] == type:
                        data_time_str = payment['datetime']
                        data_time = datetime.strptime(data_time_str, '%Y-%m-%d %H:%M:%S')
                        if (datetime.now() - data_time) > timedelta(minutes=30):
                            history['payed'].append(payment)
                            history['paying'].remove(payment)
                            history['paying'].append(new_payload)
                            self._save_data()
                            return new_payload
                        else:
                            return history
                history['paying'].append(new_payload)
                self._save_data()
                return new_payload
        if not user_found:
            new_user = {
                "user": user_email,
                "status": "active",
                "history": {
                    "paying": [new_payload],
                    "payed": []
                }
            }
            self.data['data'].append(new_user)
            self._save_data()
            return new_payload
    def _save_data(self):
        with open('data/payloads.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)
