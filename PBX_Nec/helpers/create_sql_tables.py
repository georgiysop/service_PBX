import sqlite3
import pandas as pd
import openpyxl

#Check tables and create tables
def check_table():
    with sqlite3.connect('D:\\repositories\\sqlite\\database.db') as connection:
        cursor = connection.cursor()
        
        if (cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Rings'; """)).fetchall()  == [(0,)]:
            cursor.execute('''
                    CREATE TABLE Rings
            (
                ring_id INTEGER PRIMARY KEY,
                date_start TEXT NOT NULL,
                date_time_start TEXT NOT NULL,
                amount_of_time REAL,
                number_1 TEXT NOT NULL,
                number_2 TEXT NOT NULL,
                type_ring TEXT NOT NULL
            );
            ''')
            
        if (cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Tariffs'; """)).fetchall()  == [(0,)]:
            cursor.execute('''
                    CREATE TABLE Tariffs
            (
                tariff_id INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                price REAL
            );
            ''')  
            
        if (cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Abonents'; """)).fetchall()  == [(0,)]:
            cursor.execute('''
                    CREATE TABLE Abonents
            (
                last_name TEXT NOT NULL,
                abonent_number TEXT NOT NULL,
                convert_number TEXT NOT NULL
            );
            ''')  

        if (cursor.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Accounts'; """)).fetchall()  == [(0,)]:
            cursor.execute('''
                    CREATE TABLE Accounts
            (
                account_id INTEGER PRIMARY KEY,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                level INTEGER NOT NULL
            );
            ''')
            cursor.execute('''INSERT INTO Accounts(login,password,level) VALUES ('admin','admin', 1); ''')


#add row_data to table Rings
def insert_to_table(listt):
    #listt = ['2023-10-16 10:45:27', '2023-10-16 10:50:32', 5.08, '2610', '89657438181', 'Мобильный']
    with sqlite3.connect('D:\\repositories\\sqlite\\database.db') as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Rings(date_start, date_time_start, amount_of_time, number_1, number_2, type_ring) VALUES (?, ?, ?, ?, ?, ?)", (listt[0], listt[1], listt[2], listt[3], listt[4], listt[5]))



#add row_data to table Abonents (exel to sqlite)
def insert_exeltable_to_sqlite():
    connect = sqlite3.connect('D:\\repositories\\sqlite\\database.db')
    wb = pd.read_excel('phones.xlsx',sheet_name = 'Телефоны')
    wb.to_sql(name='Abonents', con=connect, if_exists='replace', index=True)
    connect.commit()
    connect.close()



#check_table()
# insert_to_table()    
# insert_exeltable_to_sqlite()


