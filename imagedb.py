import sqlite3
sqlConn = sqlite3.connect('CustomerInfo.sqlite')
cursor = sqlConn.cursor()
cursor.execute("drop table if exists Customer")
cursor.execute("create table Customer (CustomerID INT, Image BLOB)")

def convertToBinaryData(filename):
    # Convert binary format to images
    # or files data
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData
def insertBLOB(id, photo):
    try:

        sqlite_insert_blob_query = """INSERT INTO Customer (CustomerID, Image) VALUES (?, ?)"""
        cusImage = convertToBinaryData(photo)
        dataTuple = (id, cusImage)
        cursor.execute(sqlite_insert_blob_query, dataTuple)
        sqlConn.commit()
        print("Inserted data successfully")
    except sqlite3.Error as error:
        print("Data not added", error)
insertBLOB("1", "D:\Images\Customer1.jpeg")
insertBLOB("2", "D:\Images\Customer2.jpg")
