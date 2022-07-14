import sqlite3
import xlrd
import time
# Connect to sqlite
conn = sqlite3.connect('CustomerInfo.sqlite')

# Connect to cursor
cursor = conn.cursor()
cursor.execute("drop table if exists BILL")
cursor.execute("drop table if exists Item")
cursor.execute("CREATE TABLE BILL ( ItemID INTEGER , Quantity INTEGER , Time TEXT , CustomerID INTEGER )")
cursor.execute("CREATE TABLE Item (ID INTEGER , Name TEXT , Price FLOAT , Brand TEXT, Product_Line TEXT, PRIMARY KEY(ID) )")


# Clear table
def clear_Table(tableName):
    cursor.execute("delete from " + str(tableName))


# Add Item dataset from outside
def add_Item_from_file():
    lines = open('Item.txt').readlines()
    sql = """INSERT INTO Item VALUES(?,?,?,?,?)"""
    num_line = 0
    for line in lines:
        num_line += 1
        data = line.rstrip().split()
        if (len(data)==3):
            temp = data[2]
            data.pop(2)
            data.append("null")
            data.append(temp)
        if(num_line==len(lines)): break
        try:
            name = data[0]
            price = int(float(data[1]))
            brand = data[2]
            product_line = data[3]
            cursor.execute(sql, (num_line, name, price, brand, product_line))
        except Exception as e: print(e)       
    print("Add successfully")

def viewItem():
    cursor.execute("Select * from Item")
    catcher = cursor.fetchall()
    for item in catcher:
         print("{: <10} {: <30} {: <20} {: <20} {: <30}".format(*item))


def add_Item(name, price, brand, product_line):
    sql = "INSERT INTO Item VALUES(?,?,?,?,?)"
    id = cursor.execute("Select MAX(ID) from Item")
    try:
        file = open("Item.txt", "a")
        file.write(f'{name} {price} {brand} {product_line}')
        file.close()
        cursor.execute(sql, (id+1, name, price, brand, product_line))
    except Exception as e: print(e)


def add_Bill(item_id, quantity, time, Customer_id):
    sql = "INSERT INTO Item VALUES(?,?,?,?)"
    try:
        cursor.execute(sql, (item_id, quantity, time, Customer_id))
    except Exception as e: print(e)

def add_Bill():
    Customer_id, item_id, quantity, time = getInput()
    sql = "INSERT INTO BILL VALUES(?,?,?,?)"
    try:
        cursor.execute(sql, (item_id, quantity, time, Customer_id))
    except Exception as e: print(e)

def getInput():
    t = time.localtime()
    t = time.strftime('%Y-%m-%d %H:%M:%S', t)
    Customer_id = input('Enter customer id: ')
    item_id = input('Enter item id: ')
    quantity = input('Enter quantity: ')
    return Customer_id, item_id,quantity,t

        
# Add Bill dataset from outside
def add_Bill_from_file():
    wb = xlrd.open_workbook("BillData.xls")
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    sql = """INSERT INTO BILL VALUES(?,?,?,?)"""
    num_line = 0
    for i in range(sheet.nrows):
        try:
            data = sheet.row_values(i)
            ItemID = int(data[0])
            Quantity = int(data[1])
            Time = data[2]
            CustomerID = int(data[3])
            cursor.execute(sql, (ItemID, Quantity, Time, CustomerID))
        except Exception as e: print(e)          
    print("Add bill Successfully")

def viewBill():
    cursor.execute("Select * from BILL")
    catcher = cursor.fetchall()
    if len(catcher) == 0:
        print("No order yet")
    else:
        for bill in catcher:
            print("{: <10} {: <20} {: <30} {: <10}".format(*bill))

def viewItem(ItemID):
    cursor.execute("Select * from Item where ID=?", (ItemID,))
    catcher = cursor.fetchall()
    return catcher[0][1]

# havent tested yet
def viewOrder(CustomerID):
    cursor.execute("select * from BILL where CustomerID=? order by Time desc", (CustomerID,)) 
    catcher = cursor.fetchall()
    print("| {: <30} {: <10} {: <20} |".format('Item', 'Quantity', 'Time'))
    for bill in catcher:
        Item = viewItem(bill[0])
        Quan = bill[1]
        time = bill[2]
        print("| {: <30} {: <10} {: <20} |".format(Item, Quan, time))
        
        


def isEmpty(tableName):
    cursor = conn.execute("SELECT count(*) FROM " + str(tableName))
    icount = cursor.fetchall()
    if (icount[0][0] == 0):
        return True
    else:
        return False

def checkSheet():
    wb = xlrd.open_workbook("BillData.xls")
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    for i in range(sheet.nrows):
        print(sheet.row_values(i))
