import json
from datetime import datetime, timedelta
from firebase_admin import credentials, firestore
import firebase_setup  # Khởi tạo Firebase

class Payload:
    def __init__(self) -> None:
        self.db = firestore.client()

    def payload(self, current_time, user_email, type, order_id):
        # Tạo payload mới
        new_payload = {
            "order_id_buy": order_id,
            "datetime": current_time,
            "type": type
        }

        # Truy vấn người dùng từ Firestore
        users_ref = self.db.collection('payload')
        user_doc = users_ref.document(user_email).get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            history = user_data.get('history', {})  # Trả về một từ điển rỗng nếu không có 'history'

            # Khởi tạo 'paying' và 'payed' nếu không tồn tại
            if 'paying' not in history:
                history['paying'] = []
            if 'payed' not in history:
                history['payed'] = []

            # Kiểm tra thanh toán hiện tại
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

            # Thêm mới vào danh sách thanh toán
            history['paying'].append(new_payload)
            self._save_data(user_email, history)
            return new_payload
        else:
            # Nếu không tìm thấy người dùng, tạo người dùng mới
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
        # Lưu dữ liệu vào Firestore
        self.db.collection('payload').document(user_email).set(data)