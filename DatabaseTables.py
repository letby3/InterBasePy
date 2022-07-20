import sqlite3


class PetShopTable:
    def __init__(self):
        self.conn = sqlite3.connect("ZooShop.db")
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS PetShop(PetShopID integer not null primary key, Name varchar(10) not null,
         Adress varchar(30) not null, PostalCode varchar(10) not null, City varchar(15) not null,
          Phone bigint not null)''')
        self.conn.commit()

    def insert_values(self, Name, Adress, PostalCode, City, Phone):
        self.c.execute('''INSERT INTO PetShop( Name, Adress, PostalCode, City, Phone) VALUES(?, ?, ?, ?, ?)''',
                       (Name, Adress, PostalCode, City, Phone))
        self.conn.commit()


class CustomerTable:
    def __init__(self):
        self.conn = sqlite3.connect("ZooShop.db")
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS Customer(CustomerID integer primary key, 
        LastName varchar(30) not null, FirstName integer not null,
         Adress integer not null, City integer not null, Phone bigint not null, 
         PetShopID int not null)''')
        self.conn.commit()

    def insert_values(self, LastName, FirstName, Adress, City, Phone, PetShopID):
        self.c.execute('''INSERT INTO Customer(LastName, FirstName, Adress, City, Phone, PetShopId)
         VALUES(?, ?, ?, ?, ?, ?)''',
                       (LastName, FirstName, Adress, City, Phone, PetShopID))
        self.conn.commit()

