import firebase_admin
from firebase_admin import credentials

# Kiểm tra xem Firebase đã được khởi tạo chưa
if not firebase_admin._apps:
    cred = credentials.Certificate("data/data.json")  # Đường dẫn tới tệp JSON của bạn
    firebase_admin.initialize_app(cred)
