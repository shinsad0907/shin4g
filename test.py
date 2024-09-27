from datetime import datetime

# Lấy thời gian hiện tại
now = datetime.now()

# Định dạng thời gian thành chuỗi với giờ, phút, giây
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

print("Thời gian hiện tại:", current_time)
