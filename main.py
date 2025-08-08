import os
import gspread
from google.oauth2.service_account import Credentials

#Google Sheet Setup#
service_acc_file = "D:\Coding\Python\Inventory management system\Inventory Google Sheet.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(
    service_acc_file,
    scopes=SCOPES
)
client = gspread.authorize(credentials)

SPREADSHEET_ID = '1fvdYHe0zB5eA0EbI1vaIsN4MES57GenV62PGVz390j8'
try:
    sheet = client.open_by_key('1fvdYHe0zB5eA0EbI1vaIsN4MES57GenV62PGVz390j8').sheet1
except Exception as e:
    print("Error opening Google Sheet:", e)
    sheet = None


#Save Function#
def save_inventory_to_google_sheet():
    if not sheet:
        print("Google Sheet not connected!")
        return
    sheet.clear()
    header = ['Product ID', 'Name', 'Price', 'Stock']
    sheet.append_row(header)
    for pid, info in inventory.items():
        row = [pid, info['Name'], info['Price'], info['Stock']]
        sheet.append_row(row)
    print("Inventory saved to Google Sheet.")

def load_inventory_from_google_sheet():
    if not sheet:
        print("Google Sheet not connected!")
        return
    try:
        records = sheet.get_all_records()
        global inventory
        inventory = {}
        for row in records:
            pid = int(row['Product ID'])
            inventory[pid] = {
                'Name': row['Name'],
                'Price': float(row['Price']),
                'Stock': int(row['Stock'])
            }
        print("Inventory loaded from Google Sheet.")
    except Exception as e:
        print("Failed to load inventory:", e)


inventory = {} #Format : {product_id {'Name'-str, 'Price'-float, 'Stock'-int}}
orders = [] #List of all orders

#Functions#

def add_product():
    product_id = int(input("Enter product ID : "))
    if product_id in inventory:
        print("Product ID already exists!")
        return
    name = input("Enter product Name : ")
    price = float(input("Enter Price : "))
    stock = int(input("Enter stock Quantity : "))
    
    inventory[product_id] = {'Name':name, 'Price':price, 'Stock':stock}
    print("Product added successfully")
    save_inventory_to_google_sheet()

def update_product():
    product_id = int(input("Enter Product ID : "))
    if product_id not in inventory:
        print("Product not found!!")
        return
    print("Current Info : ",inventory[product_id])
    name = input("Enter new name (Leave blank to keep same) : ")
    price = input("Enter new price (Leave blank to keep same) : ")
    stock = input("Enter new quantity (Leave blank to keep same) : ")

    if name:
        inventory[product_id]['Name'] = name
    if price:
        inventory[product_id]['Price'] = float(price)
    if stock:
        inventory[product_id]['Stock'] = int(stock)
    print("Product updated!")
    save_inventory_to_google_sheet()

def delete_product():
    product_id = int(input("Enter Product ID : "))
    if product_id in inventory:
        del inventory[product_id]
        print("Product deleted")
    else:
        print("Product not found")
    save_inventory_to_google_sheet()

def view_inventory():
    if not inventory:
        print("Inventory is Empty :()")
        return
    print("INVENTORY : \n")
    for pid,info in inventory.items():
        print(f"ID : {pid} | Name : {info['Name']} | Price : {info['Price']} | Stock : {info['Stock']}")
    save_inventory_to_google_sheet()

def take_order():
    product_id = int(input("Enter product ID : "))
    if product_id not in inventory:
        print("Product not found!!")
        return
    quantity = int(input("Enter Quantity : "))
    if quantity > inventory[product_id]['Stock']:
        print("Not enough stock")
        return
    total = quantity * inventory[product_id]['Price']
    inventory[product_id]['Stock'] -= quantity

    order = {
        'Product ID':product_id,
        'Product Name':inventory[product_id]['Name'],
        'Quantity':quantity,
        'Total Price':total
    }
    orders.append(order)
    print(f"Order placed! Total : {total:.2f} BDT")
    save_inventory_to_google_sheet()

def view_orders():
    if not orders:
        print("No order placed yet")
        return
    print("Order History : \n")
    for i,order in enumerate(orders,start=1):
        print(f"Index : {i} | Product ID : {order['Product ID']} | Product Name : {order['Product Name']} | Qty : {order['Quantity']} | Total Price : {order['Total Price']}")
    save_inventory_to_google_sheet()
 
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


#Main Loop#

def main():
    load_inventory_from_google_sheet()
    while True:
        print("=========== Inventory & Order Management System ============ \n")
        print("1. Add Product")
        print("2. update Product")
        print("3. Delete Product")
        print("4. View Inventory")
        print("5. Take Order")
        print("6. View Order")
        print("7. Clear Screen")
        print("0. Exit")

        choice = int(input("Enter an Option : "))

        if choice == 1:
            add_product()
        elif choice == 2:
            update_product()
        elif choice == 3:
            delete_product()
        elif choice == 4:
            view_inventory()
        elif choice == 5:
            take_order()
        elif choice == 6:
            view_orders()
        elif choice == 7:
            clear_screen()
        elif choice == 0:
            print("Exiting.....")
            break
        else:
            print("Invalid Choice!")
        

if __name__ == "__main__":
    main()