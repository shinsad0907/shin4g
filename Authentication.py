import json

class Authentication:
    def __init__(self) -> None:
        with open('data/Authentication.json','r') as f:
            self.data = json.load(f)
    def data_login(self,gmail,password):
        for i in range(len(self.data['user'])):
            print(self.data['user'][i]['gmail'],self.data['user'][i]['password'])
            if self.data['user'][i]['gmail'] == gmail and self.data['user'][i]['password'] == password:
                status = 'Login Success'
                break
            else:
                status = 'Gmail & Password Wrong'
        return status
    def data_register(self,gmail,password,awaypassword):
        for i in range(len(self.data['user'])):
            if self.data['user'][i]['gmail'] == gmail:
                status = 'Gmail is using'
                break
            else:
                if password == awaypassword:
                    new_account = {
                        "gmail": gmail,
                        "password": password
                    }
                    self.data['user'].append(new_account)
                    with open('data/Authentication.json', 'w') as file:
                        json.dump(self.data, file, indent=4)
                        status = 'save success'
                        break
                else:
                    status = 'Awaypassword wrong'
                    break
        return status

