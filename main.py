import tkinter as tk
import pandas as pd
from tkinter import ttk
from DatabaseTables import *
from collections import Counter


class PetShopDialog(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = petshopvalues
        self.view_values()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="button_grey_add.png")
        btn_open_dialog = tk.Button(toolbar, text='Add', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='database_download.png')
        btn_edit_dialog = tk.Button(toolbar, text='Edit', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='button_grey_delete.png')
        btn_delete_dialog = tk.Button(toolbar, text='Delete', bg='#d7d8e0', bd=0, image=self.delete_img,
                                      compound=tk.TOP, command=self.delete_values)
        btn_delete_dialog.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='zoom_in.png')
        btn_search_dialog = tk.Button(toolbar, text='Search', bg='#d7d8e0', bd=0, image=self.search_img,
                                      compound=tk.TOP, command=self.search_diaolog)
        btn_search_dialog.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.png')
        btn_search_dialog = tk.Button(toolbar, text='Refresh', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                      compound=tk.TOP, command=self.view_values)
        btn_search_dialog.pack(side=tk.LEFT)

        btn_customer_table = tk.Button(toolbar, text='Finished the programs', command=self.customer_table, bg='#d7d8e0', bd=0,
                                       compound=tk.TOP)
        btn_customer_table.pack(side=tk.RIGHT)

        self.tree = ttk.Treeview(self, columns=('TableNum', 'Name', 'Email', 'Programm', 'DateStart', 'DateEnd'),
                                 height=29, show='headings')

        self.tree.column('TableNum', width=130, anchor=tk.CENTER)
        self.tree.column('Name', width=150, anchor=tk.CENTER)
        self.tree.column('TableNum', width=235, anchor=tk.CENTER)
        self.tree.column('Programm', width=155, anchor=tk.CENTER)
        self.tree.column('DateStart', width=155, anchor=tk.CENTER)
        self.tree.column('DateEnd', width=150, anchor=tk.CENTER)
        #TableNum Name Email Programm DateStart  DateEnd
        self.tree.heading('TableNum', text='Num', command=self.sort_values_by_id)
        self.tree.heading('Name', text='Name', command=self.sort_values_by_name)
        self.tree.heading('Email', text='TableNum', command=self.sort_values_by_adress)
        self.tree.heading('Programm', text='Programm', command=self.sort_values_by_postalcode)
        self.tree.heading('DateStart', text='DateStart', command=self.sort_values_by_city)
        self.tree.heading('DateEnd', text='DateEnd', command=self.sort_values_by_phone)

        self.tree.pack()

    def open_dialog(self):
        AddPetShop()

    def open_update_dialog(self):
        UpdatePetShop()

    def search_diaolog(self):
        SearchPetShop()

    def add_values(self, Name, Adress, PostalCode, City, Phone):
        self.db.insert_values( Name, Adress, PostalCode, City, Phone)
        self.view_values()

    def view_values(self):
        self.db.c.execute("SELECT * FROM PetShop")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]
        #self.tree.insert('', 'end', values = TableNum)

    def update_values(self, Name, Adress, PostalCode, City, Phone):
        self.db.c.execute('''UPDATE PetShop SET Name=?, Adress=?, City=?, PostalCode=?, Phone=? WHERE PetShopID=?''',
                          (Name, Adress, PostalCode, City, Phone, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_values()

    def search_values(self, Name):
        Name = ('%' + Name + '%',)
        self.db.c.execute('''SELECT * FROM PetShop WHERE Name LIKE ?''', Name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_values(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM PetShop WHERE PetShopID=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_values()

    def sort_values_by_id(self):
        self.db.c.execute('SELECT * FROM PetShop ORDER BY PetShopID')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_name(self):
        self.db.c.execute('SELECT * FROM PetShop ORDER BY Name')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_adress(self):
        self.db.c.execute('SELECT * FROM PetShop ORDER BY Adress')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_postalcode(self):
        self.db.c.execute('SELECT * FROM PetShop ORDER BY PostalCode')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_city(self):
        self.db.c.execute('SELECT * FROM PetShop ORDER BY City')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_phone(self):
        self.db.c.execute('SELECT * FROM PetShop ORDER BY Phone')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def customer_table(self):
        CustomerDialog()


class AddPetShop(tk.Toplevel):
    def __init__(self):
        super().__init__(pet_shop_dialog)
        self.init_child()
        self.view = pet_shop_table

    def init_child(self):
        self.title("Insert Values")
        self.geometry('600x400')
        self.resizable(False, False)


        label_name = tk.Label(self, text='Name:')
        label_name.place(x=180, y=50)
        label_adress = tk.Label(self, text='Adress:')
        label_adress.place(x=180, y=80)
        label_postal_code = tk.Label(self, text='PostalCode:')
        label_postal_code.place(x=180, y=110)
        label_city = tk.Label(self, text='City:')
        label_city.place(x=180, y=140)
        label_phone = tk.Label(self, text='Phone:')
        label_phone.place(x=180, y=170)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=325, y=50)

        self.entry_adress = ttk.Entry(self)
        self.entry_adress.place(x=325, y=80)

        self.entry_postal_code = ttk.Entry(self)
        self.entry_postal_code.place(x=325, y=110)

        self.entry_city = ttk.Entry(self)
        self.entry_city.place(x=325, y=140)

        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=325, y=170)

        btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=350, y=300)

        self.btn_add = ttk.Button(self, text='Add')
        self.btn_add.place(x=200, y=300)
        self.btn_add.bind('<Button-1>', lambda event: self.view.add_values(self.entry_name.get(),
                                                                           self.entry_adress.get(),
                                                                           self.entry_postal_code.get(),
                                                                           self.entry_city.get(),
                                                                           self.entry_phone.get()))


class UpdatePetShop(AddPetShop):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = pet_shop_table

    def init_edit(self):
        self.title('Edit')
        btn_edit = ttk.Button(self, text='Edit')
        btn_edit.place(x=200, y=300)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_values(self.entry_name.get(),
                                                                          self.entry_adress.get(),
                                                                          self.entry_postal_code.get(),
                                                                          self.entry_city.get(),
                                                                          self.entry_phone.get()))
        self.btn_add.destroy()


class SearchPetShop(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = pet_shop_table

    def init_search(self):
        self.title('Search For Values')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Name: ')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Search')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_values(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class CustomerDialog(tk.Toplevel):
    def __init__(self):
        super().__init__(pet_shop_dialog)
        self.init_customer()
        self.db = CustomerTable()
        self.view_values()

    def init_customer(self):
        self.title("Finished the programs")
        self.geometry("1550x715")
        self.resizable(False, False)

        self.add_img = tk.PhotoImage(file="button_grey_add.png")
        btn_open_dialog = tk.Button(self, text='Add', command=self.open_dialog_customer, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img, padx="10", pady="3", font="10")
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='database_download.png')
        btn_edit_dialog = tk.Button(self, text='Edit', command=self.update_dialog_customer, bg='#d7d8e0', bd=0,
                                    image=self.update_img, compound=tk.TOP, padx="10", pady="3", font="10")
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='button_grey_delete.png')
        btn_delete_dialog = tk.Button(self, text='Delete', bg='#d7d8e0', bd=0, image=self.delete_img,
                                      compound=tk.TOP, padx="10", pady="3", font="10", command=self.delete_customer)
        btn_delete_dialog.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='zoom_in.png')
        btn_search_dialog = tk.Button(self, text='Search', bg='#d7d8e0', bd=0, image=self.search_img,
                                      compound=tk.TOP, padx="10", pady="3", font="10", command=self.search_diaolog)
        btn_search_dialog.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.png')
        btn_search_dialog = tk.Button(self, text='Refresh', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                      compound=tk.TOP, padx="10", pady="3", font="10", command=self.view_values)
        btn_search_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('CustomerID', 'LastName', 'FirstName'),
                                 height=34, show='headings')

        self.tree.column('CustomerID', width=170, anchor=tk.CENTER)
        self.tree.column('LastName', width=200, anchor=tk.CENTER)
        self.tree.column('FirstName', width=190, anchor=tk.CENTER)
        '''
        self.tree.column('Adress', width=200, anchor=tk.CENTER)
        self.tree.column('City', width=150, anchor=tk.CENTER)
        self.tree.column('Phone', width=170, anchor=tk.CENTER)
        self.tree.column('PetShopID', width=90, anchor=tk.CENTER)
        '''
        self.tree.heading('CustomerID', text='Num', command=self.sort_values_by_customerid)
        self.tree.heading('LastName', text='ProgrammName', command=self.sort_values_by_lastname)
        self.tree.heading('FirstName', text='Count', command=self.sort_values_by_firstname)
        '''
        self.tree.heading('Adress', text='Adress', command=self.sort_values_by_adress)
        self.tree.heading('City', text='City', command=self.sort_values_by_city)
        self.tree.heading('Phone', text='Phone', command=self.sort_values_by_phone)
        self.tree.heading('PetShopID', text='PetShopID', command=self.sort_values_by_petshopid)
        '''
        self.tree.pack()

    def add_customer(self, LastName, FirstName, Adress, City, Phone, PetShopID):
        self.db.insert_values(LastName, FirstName, Adress, City, Phone, PetShopID)
        #self.view_values()

    def view_values(self):
        self.db.c.execute('''SELECT PostalCode FROM PetShop''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        NewM1 = self.db.c.fetchall()
        #print(NewM1[0][0])
        NewM = []
        for i in NewM1:
            #print(i[0])
            NewM.append(i[0])
        Countt = Counter(NewM)
        print(Countt)
        self.db.c.execute('''DELETE FROM Customer;''',)
        for i in Countt:
            self.add_customer(i, Countt[i], 0, 0, 0, 0)
        self.db.c.execute('''SELECT * FROM Customer''')
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def update_customer(self, LastName, FirstName, Adress, City, Phone, PetShopID):
        self.db.c.execute('''UPDATE Customer SET LastName=?, FirstName=?, Adress=?, City=?, Phone=?,
         PetShopID=? WHERE CustomerID=?''',
                          (LastName, FirstName, Adress, City, Phone, PetShopID,
                           self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_values()

    def search_customer(self, LastName):
        LastName = ('%' + LastName + '%',)
        self.db.c.execute('''SELECT * FROM Customer WHERE LastName LIKE ?''', LastName)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_customer(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM Customer WHERE CustomerID=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_values()

    def sort_values_by_customerid(self):
        self.db.c.execute('SELECT * FROM Customer ORDER BY CustomerID')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_lastname(self):
        self.db.c.execute('SELECT * FROM Customer ORDER BY LastName')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_firstname(self):
        self.db.c.execute('SELECT * FROM Customer ORDER BY FirstName')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_adress(self):
        self.db.c.execute('SELECT * FROM Customer ORDER BY Adress')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_city(self):
        self.db.c.execute('SELECT * FROM Customer ORDER BY City')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_phone(self):
        self.db.c.execute('SELECT * FROM Customer ORDER BY Phone')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_values_by_petshopid(self):
        self.db.c.execute('SELECT * FROM Customer ORDER BY PetShopID')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog_customer(self):
        AddCustomer(self)

    def update_dialog_customer(self):
        UpdateCustomer(self)

    def search_diaolog(self):
        SearchCustomer(self)


class AddCustomer(tk.Toplevel):
    def __init__(self, CustomerDialog):
        super().__init__(pet_shop_dialog)
        self.init_child()
        self.view = CustomerDialog

    def init_child(self):
        self.title("Insert Values")
        self.geometry('600x400')
        self.resizable(False, False)

        label_lastname = tk.Label(self, text='Programm:')
        label_lastname.place(x=180, y=50)
        label_firstname = tk.Label(self, text='Count:')
        label_firstname.place(x=180, y=80)

        '''
        label_adress = tk.Label(self, text='Adress:')
        label_adress.place(x=180, y=110)
        label_city = tk.Label(self, text='City:')
        label_city.place(x=180, y=140)
        label_phone = tk.Label(self, text='Phone:')
        label_phone.place(x=180, y=170)
        label_petshopid = tk.Label(self, text='PetShopID:')
        label_petshopid.place(x=180, y=200)
        '''

        self.entry_lastname = ttk.Entry(self)
        self.entry_lastname.place(x=325, y=50)

        self.entry_firstname = ttk.Entry(self)
        self.entry_firstname.place(x=325, y=80)
        '''
        self.entry_adress = ttk.Entry(self)
        self.entry_adress.place(x=325, y=110)

        self.entry_city = ttk.Entry(self)
        self.entry_city.place(x=325, y=140)

        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=325, y=170)

        self.entry_petshopid = ttk.Entry(self)
        self.entry_petshopid.place(x=325, y=200)
        '''
        btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=350, y=300)

        self.btn_add = ttk.Button(self, text='Add')
        self.btn_add.place(x=200, y=300)
        self.btn_add.bind('<Button-1>', lambda event: self.view.add_customer(self.entry_lastname.get(),
                                                                             self.entry_firstname.get(),
                                                                             0,
                                                                             0,
                                                                             0,
                                                                             0))


class UpdateCustomer(AddCustomer):
    def __init__(self, CustomerDialog):
        super().__init__(pet_shop_dialog)
        self.init_edit()
        self.view = CustomerDialog

    def init_edit(self):
        self.title('Edit')
        btn_edit = ttk.Button(self, text='Edit')
        btn_edit.place(x=200, y=300)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_customer(self.entry_lastname.get(),
                                                                            self.entry_firstname.get(),
                                                                            self.entry_adress.get(),
                                                                            self.entry_city.get(),
                                                                            self.entry_phone.get(),
                                                                            self.entry_petshopid.get()))

        self.btn_add.destroy()


class SearchCustomer(tk.Toplevel):
    def __init__(self, CustomerDialog):
        super().__init__()
        self.init_search()
        self.view = CustomerDialog

    def init_search(self):
        self.title('Search For Values')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='LastName:')
        label_search.place(x=40, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Close', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Search')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_customer(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')




def AddExcelFile():
    file = pd.read_excel(io = '62543c705a6b1.xlsx', sheet_name = 'Тренинги',
                         usecols='A:H')
    ProgrammName = file['Программа'].tolist()
    DateStart = file['Дата начала'].tolist()
    DateEnd = file['Дата окончания'].tolist()
    Names = file['Сотрудник (RU)'].tolist()
    TableNum = file['Табельный номер'].tolist()
    eMail = file['E-mail'].tolist()
    '''
    Custm = CustomerDialog()
    '''
    Count = Counter(ProgrammName)
    print(Count)
    '''
    for i in Count:
        Custm.add_customer(i, Count[i], 0, 0 ,0, 0)
    '''
    for i in range(0, len(Names) - 1):
        pet_shop_table.add_values(Names[i], TableNum[i], ProgrammName[i], DateStart[i], DateEnd[i])

if __name__ == "__main__":

    pet_shop_dialog = tk.Tk()
    petshopvalues = PetShopTable()
    pet_shop_table = PetShopDialog(pet_shop_dialog)
    pet_shop_table.pack()

    #AddExcelFile()

    pet_shop_dialog.title("DataBase")
    pet_shop_dialog.geometry("1020x700+300+200")
    pet_shop_dialog.resizable(False, False)

    pet_shop_dialog.mainloop()
