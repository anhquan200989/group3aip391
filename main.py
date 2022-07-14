# import data, item, bill
from Database.Database_handle.Data_handle import *

# add items
add_Item_from_file()
# viewItem()
print('-' * 110)
# add bill
add_Bill_from_file()
viewBill()
print('-' * 110)

viewOrder(5)
# import picture data
from Database.ImageDatabase import *
#-----------------------------------------------------------------------------------
from Database.final.mp_checkout import *

# when customer enters the store
# create face_recognition

# create face_detection (return customer id)

# return customer's id (to database get bill)

# return the bill from id

#-------------------------------------------------------------------------------------
# when customer checkout

# main()
