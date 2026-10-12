class AdminAccount:
    def __init__(self, username, password):
        self.username = username
        self.__password=password

    def login(self, username, password):
        if self.username == username and self.__password == password:
            return("login sukses")
        else:
            return("login gagal")

account1=AdminAccount("jokowi123", "GlbandGlbb")
account2=AdminAccount("Prabowo321", "202020")
print(account1.login("jokowi321", "GlbandGlbb"))
print(account1.login("jokowi123", "manuk"))
print(account1.login("jokowi123", "GlbandGlbb"))
print(account2.login("Prabowo321", "202020"))
