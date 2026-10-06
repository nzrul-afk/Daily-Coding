class User:
    def get_access(self):
        print("Akses level: User biasa")

class Admin(User):
    def get_access(self):
        print("Akses level: Administrator")


usernya = User()
usernya.get_access()
Admin = Admin()
Admin.get_access()