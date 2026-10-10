class Player:
    def __init__ (self, userName, level, hp):
        self.userName = userName
        self.level = level
        self.hp = hp
    def add(self,levelup):
        self.level += levelup

player1 = Player("Nasrul", 0, 5000)
print(player1.userName)
print(player1.level)
player1.add(20)
player1.add(19)
print(player1.level)
