import firebase_admin
from firebase_admin import credentials, firestore
import firebase_setup  # Khởi tạo Firebase

class Authentication:
    def __init__(self) -> None:
        self.db = firestore.client()  # Kết nối với Firestore

    def data_login(self, gmail, password):
        users_ref = self.db.collection('Authentication')
        users = users_ref.stream()

        status = 'Gmail & Password Wrong'
        for user in users:
            user_data = user.to_dict()
            if user_data['gmail'] == gmail and user_data['password'] == password:
                status = 'Login Success'
                break
        
        return status

    def data_register(self, gmail, password, awaypassword):
        users_ref = self.db.collection('Authentication')
        users = users_ref.stream()

        status = 'save success'
        for user in users:
            user_data = user.to_dict()
            
            # Kiểm tra xem 'gmail' có trong user_data không
            if 'gmail' in user_data and user_data['gmail'] == gmail:
                status = 'Gmail is using'
                break
        
        if status == 'save success' and password == awaypassword:
            new_account = {
                'gmail': gmail,
                'password': password
            }
            users_ref.add(new_account)
        elif password != awaypassword:
            status = 'Awaypassword wrong'

        return status

