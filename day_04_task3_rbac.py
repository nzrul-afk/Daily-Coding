class User:
    def __init__(self, name, password, role):
        self.name=name
        self.password=password
        if role.lower() == "admin":
            self.role="admin"
        else:
            self.role="user"
        self.locked_account=False

class AuthSystem:
    def __init__(self):
        self.db_account = []

    def register(self, user_obj):
        self.db_account.append(user_obj)

    def login(self, name, password):
        failed_login=0
        
        for i in self.db_account:
            if i.locked_account == True:
                print("akun terkunci")
                break
            if name == i.name and password == i.password:
                failed_login=0
                if i.role == "admin":
                    print("selamat datang admin")
                    break
                else:
                    print("selamar datang")

            else:
                failed_login +=1
                print("name atau password anda salah")
            if failed_login >= 3:
                i.locked_account = True


sistem_auth = AuthSystem()
sistem_auth.register(User("nasrul", "123", "admin"))
sistem_auth.register(User("karyawan", "abc", "USER"))
sistem_auth.login("nasrul", "salah1")
sistem_auth.login("nasrul", "salah2")
sistem_auth.login("nasrul", "123")
            

                


