import sqlite3

class Sale:
    def __init__(self, data, product, price) -> None:
        self.data = data
        self.product = product
        self.price = price

    def show(self):
        return f"data: {self.data} product: {self.product} price: {self.price}"

    def list_to_dict(self, dict, append_to_dict):
        dict = {
            "data": self.data,
            "product": self.product,
            "price": self.price
        }
        append_to_dict.append(dict)

    def create_database(self, path):
       
        con = sqlite3.connect(path)
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS Monthly_expenses(date TEXT, product TEXT, price INTEGER)"""
        )
        cur.execute(
            """INSERT INTO Monthly_expenses VALUES (?, ?, ?)""",
            (self.data, self.product, self.price)
        )
        con.commit()
        con.close()


    

class Day:
    def __init__(self, day, data) -> None:
        self.day = day
        self.data = data

    def searching(self, us_input):
        found = False
        for expens in self.data:
            if us_input == expens.product:
                print(f"found {expens.show()}")
                found = True
        return found

    def total_price(self):
        return sum(sale.price for sale in self.data)
