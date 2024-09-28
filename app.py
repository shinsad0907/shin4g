from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
import firebase_admin
from Authentication import Authentication
from firebase_admin import credentials, firestore, auth
from payload import Payload
import random

cred = credentials.Certificate('data/data.json')  # Đường dẫn đến tệp JSON
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.secret_key = '1c2416c5bc4eba1897aa21ac6b724ee7879199dd70d1967e'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(email):
    user = User()
    user.id = email
    return user

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        awaypassword = request.form['awaypassword']
        status_login = Authentication().data_register(email, password, awaypassword)

        if status_login == 'Gmail is using':
            flash('Email đã được đăng ký!')
        else:
            if status_login == 'Register Success':
                flash('Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.')
            else:
                flash('Mật Khẩu Nhập Lại Không Giống')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        status_login = Authentication().data_login(email, password)

        if status_login == 'Login Success':
            user = User()
            user.id = email
            login_user(user)
            return redirect(url_for('home_page'))
        else:
            flash('Thông tin đăng nhập không chính xác!')
    return render_template('login.html')

login_manager.login_view = 'login'

@app.route('/home_page')
@login_required
def home_page():
    return render_template('home_page.html')

@app.route('/document')
@login_required
def document():
    return render_template('document.html')

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/payment')
@login_required
def payment():
    user_email = current_user.id

    speed = request.args.get('speed', 'Tối Đa 2 Gbps')
    storage = request.args.get('storage', '512 GB')
    device_limit = request.args.get('device_limit', 'Id: 2 Thiết Bị/Gói')
    support = request.args.get('support', 'ADR - IOS')
    price = request.args.get('price', '10,000đ')

    order_id_buy = generate_order_id()
    order_id = datetime.now().strftime("%Y%m%d%H%M%S")
    order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    package_info = {
        'name': 'Gói VIP',
        'speed': speed,
        'data': storage,
        'devices': device_limit,
        'support': support,
        'sms': 'VINA Soạn YT30 gửi 888',
        'price': price,
        'order_id_buy': order_id_buy
    }

    session['payment_user'] = {
        'email': user_email,
        'order_id': order_id,
        'package': package_info,
        'time': order_time,
    }

    return render_template('payment.html', order_id_buy=order_id_buy, order_id=order_id, order_time=order_time, package=package_info)

def generate_order_id():
    time_component = datetime.now().strftime("%Y%m%d%H%M%S")
    random_component = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return time_component + random_component

@app.route('/QR')
@login_required
def QR():
    payment_info = session.get('payment_user')
    type = payment_info['package']['name']
    order_id = payment_info['package']['order_id_buy']
    price = payment_info['package']['price']

    user_email = current_user.id
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    data = Payload().payload(current_time, user_email, type, order_id)
    if 'paying' in data and data['paying']:
        for payment in data['paying']:
            if payment_info['package']['name'] == payment['type']:
                order_time = payment['datetime']
                order_id_buy = payment['order_id_buy']
                break
        else:
            order_time = current_time
            order_id_buy = order_id
    else:
        order_time = current_time
        order_id_buy = order_id

    order_time = datetime.strptime(order_time, '%Y-%m-%d %H:%M:%S')
    time_remaining = (order_time + timedelta(minutes=30)) - now
    
    if time_remaining.total_seconds() < 0:
        time_remaining_seconds = 0
    else:
        time_remaining_seconds = int(time_remaining.total_seconds())

    return render_template('QR.html', time_remaining_seconds=time_remaining_seconds, package_info=order_id_buy, price=price)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
