class Book:
    def __init__(self, title, author, is_borrow=False):
        self.title = title
        self.author = author
        self.mybook = []
    def check_myborrowing_book(self):
        if self.mybook == []:
            return("kamu belum meminjam buku")
        for index,i in enumerate(self.mybook):
            print(f'{index + 1}. {i}')

    def borrow_book(self, title):
        is_borrow=True
        self.mybook.append(title)
        print(f"Buku {self.title} berhasil dipinjam")
        print(is_borrow)
    
    def mengembalikan_book(self, title):
        is_borrow=False
        self.mybook.remove(title)
        print(f"Buku {self.title} berhasil dikembalikan")

buku1= Book("islam ala prabowo", "jokowi")
buku1.borrow_book("islam ala prabowo")
buku1.check_myborrowing_book()
buku1.mengembalikan_book("islam ala prabowo")
buku1.check_myborrowing_book()