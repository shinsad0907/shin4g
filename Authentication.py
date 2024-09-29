import requests

url = "https://66f957adafc569e13a9882cf.mockapi.io/Authentication"
headers = {
    "Authorization": "66f957adafc569e13a9882cf",
    "Content-Type": "application/json"
}

class Authentication:
    def data_login(self, gmail, password):
        response = requests.get(url, headers=headers)
        users = response.json()

        status = 'Gmail & Password Wrong'
        for user in users:
            if 'gmail' in user and user['gmail'] == gmail and user['password'] == password:
                status = 'Login Success'
                break
        
        return status

    def data_register(self, gmail, password, awaypassword):
        response = requests.get(url, headers=headers)
        users = response.json()

        status = 'save success'
        for user in users:
            if 'gmail' in user and user['gmail'] == gmail:
                status = 'Gmail is using'
                break
        
        if status == 'save success' and password == awaypassword:
            new_account = {
                'gmail': gmail,
                'password': password
            }
            response = requests.post(url, headers=headers, json=new_account)
            if response.status_code == 201:  # Kiểm tra nếu tạo mới thành công
                status = 'User registered successfully!'
            else:
                status = 'Error in registration'
        elif password != awaypassword:
            status = 'Awaypassword wrong'

        return status
