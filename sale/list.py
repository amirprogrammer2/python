from clases import Sale, Day
import json
import sqlite3
file_name = "month.json"
path = "Monthly_expenses.db"
all = []
all_expenses = []
all_to_dict = {}

con = sqlite3.connect(path)
cur = con.cursor()
cur.execute(" SELECT * FROM Monthly_expenses ")
get_data = cur.fetchall()
for row in get_data:
    print(row)
for day in range(1, 3):
    budget = int(input("budget of week: "))
    sale_week = Day(day, [])
    print(f"day {day}")

    while True:
        data = input("enter data or 'exit': ")

        if data == "exit":
            break
        product = input("enter your reason: ")
        price = int(input("enter price: "))

        budget -= price
        if budget >= 0:
            print(f"u have {budget} left")
        else:
            print("ur budget is done")
            break

        sale = Sale(data, product, price)
        sale_week.data.append(sale)

        sale.list_to_dict(all_to_dict, all_expenses)

        sale.create_database(path)

    all.append(sale_week)

choice = input("search product and data or all? ")
if choice == "all":
    for dayofweek in all:
        print(f"day {dayofweek.day}")
        for kharj in dayofweek.data:
            print(f"{kharj.show()}")

elif choice in ["search", "data"]:
    user_search = input("search here: ")
    found = False
    for sea in all:
        if sea.searching(user_search):
            found = True
            break
    if not found:
        print("sikter")


with open(file_name, 'a') as json_file:
    json.dump(all_expenses, json_file, indent=4)
