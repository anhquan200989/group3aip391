import glob
import sqlite3
sqlConn = sqlite3.connect('CustomerInfo.sqlite')
cursor = sqlConn.cursor()
cursor.execute("drop table if exists Customer")
cursor.execute("create table Customer (CustomerID INT, Image BLOB)")
id = 0
dir_path = r'D:\Images\*.*'
def convertToBinaryData(filename):
    # Convert binary format to images
    # or files data
    with open(filename, 'rb') as ifile:
        blobData = ifile.read()
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

res = glob.glob(dir_path)
for item in res:
    id += 1
    insertBLOB(id, item)
