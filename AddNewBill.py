from Data_handle import *

'''
tạo chương trình quản lí bill
thêm vào database, input bàn phím
'''
# loop until user wants to exit
while True:
    print('Bill Managerment')
    print('1: Add new bill')
    print('2. View bill')
    print('3: Exit')
    # user enters their choice
    userInput = input('Enter your choice: ')
    if userInput == '1':
        add_Bill()
    elif userInput == '2':
        viewBill()
    elif userInput == '3':
        break