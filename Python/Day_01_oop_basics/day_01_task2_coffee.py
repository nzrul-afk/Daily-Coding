class CoffeeOrder:
    def __init__(self, menu, size, status='pending'):
        self.menu = menu
        self.size = size
        
        self.status = status

pesanan1 = CoffeeOrder("martabak", 20)
pesanan2 = CoffeeOrder("geprek", 19, "Completed")

print(pesanan1.status)