#  Coffee Shop Management

import sys
import csv
import re


class Shop():
    def __init__(self, investment, total_revenue, zip, name):
        self.investment = investment
        self.total_revenue = total_revenue
        self.zip = zip
        self.name = name

    def __str__(self):
        return f"{self.name} in zipcode: {self.zip} has total investment of ${self.investment} and total revenue of ${self.total_revenue}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def zip(self):
        return self._zip

    @zip.setter
    def zip(self, zip):
        self._zip = zip

    @property
    def investment(self):
        return self._investment

    @investment.setter
    def investment(self, investment):
        self._investment = investment

    @property
    def total_revenue(self):
        return self._total_revenue

    @total_revenue.setter
    def total_revenue(self, total_revenue):
        self._total_revenue = total_revenue


def main():
    # Getting email
    email = input("Enter your authorized email: ").strip()
    check = verify_email(email)
    if not check:
        sys.exit("Please enter authorized email only, no personal email allowed! Try re-login")

    print("")
    print("***Welcome, you are logged in, please provide accurate information in upcoming steps***")
    print("")

    #Getting the shop details
    name, zip, investment, total_revenue = shop_detail()
    shop = Shop(investment, total_revenue, zip, name)

    #Getting to know that user wants to do
    number = requirement()
    if number == "1":
        invest(shop)
    elif number == "2":
        sell(shop)
    elif number == "3":
        storage(shop)
    else:
        profit(shop)
    print("")
    sys.exit("Please re-login to perform another task")


def verify_email(email):
    #verifying email using library re
    if re.search(r"^[^@]+@(coffee\.com|COFFEE\.COM)$", email, re.IGNORECASE):
        return True
    else:
        return False


def shop_detail():
    #Getting name of shop
    while True:
        name = input("Enter your shop name: ").strip()
        name = name.lower()
        if not name:
            print("Please enter proper name")
        else:
            break

    #Getting zip code of the shop
    while True:
        zip = input("Enter 5-digit shop zipcode: ").strip()
        if not zip:
            print("Please enter zipcode")
            continue
        correct = zip.isdigit()
        if len(zip) != 5 or not correct:
            print("Please enter valid zipcode")
        else:
            break

    #Getting the total revenue and investment of the entered shop if it exist
    found = False
    file = open("stores.csv", "r")
    reader = csv.DictReader(file)
    for row in reader:
        if row["name"] == name and row["zip"] == zip:
            investment = row["investment"]
            total_revenue = row["total_revenue"]
            found = True
    file.close()

    #Adding the shop to the file if it doesn't exist
    if not found:
        investment = 0
        total_revenue = 0
        file = open("stores.csv", "a")
        writer = csv.DictWriter(file, fieldnames = ["name","zip","investment","total_revenue"])
        writer.writerow({"name":name,"zip":zip,"investment":investment,"total_revenue":total_revenue})
        file.close()
    return name, zip, investment, total_revenue


def requirement():
    #To know what task user wants to perform
    print("What you want to do?")
    print("Press 1: If new stock arrived")
    print("Press 2: To sell a product")
    print("Press 3: To check storage")
    print("Press 4: To check total profit")
    while True:
        number = input("Enter: ")
        if len(number) != 1 or not number.isdigit():
            print("Enter 1, 2, 3 or 4")
        else:
            break
    return number


def invest(shop):
    #Getting the name of the ingredient
    while True:
        ingredient = input("Enter name of ingredient: ").lower()
        if not ingredient:
            print("Please enter proper name of ingredient")
        else:
            break

    #Getting the weight of the ingredient
    while True:
        weight = input("Enter weight of ingredient(kg/litre): ")
        if not weight:
            print("Please enter correct weight")
        else:
            if re.search(r"^[0-9]+(\.[0-9]+)?$", weight):
                break
            else:
                print("Enter weight in either decimal or whole number")

    #Getting the toal price of the ingredient
    while True:
        price = input("Enter total price of purchase: ")
        if not price:
            print("Please enter correct cost")
        else:
            if re.search(r"^[0-9]+(\.[0-9]+)?$", price):
                break
            else:
                print("Enter price in correct numeric format")

    #Adding the details of the recent purchase to the file
    file = open("purchase.csv", "a")
    writer = csv.DictWriter(file, fieldnames = ["name","zip","ingredient","weight","price"])
    writer.writerow({"name":shop.name,"zip":shop.zip,"ingredient":ingredient,"weight":weight,"price":price})
    file.close()

    #Increasing the weight of the recently purchased ingredient in the inventory
    file = open("inventory.csv", "r")
    reader = csv.DictReader(file)
    present = False
    items = []
    for row in reader:
        items.append(row)
        if row["name"] == shop.name and row["zip"] == shop.zip and row["ingredient"] == ingredient:
            present = True
    file.close()

    if present == True:
        for element in items:
            if element["name"] == shop.name and element["zip"] == shop.zip and element["ingredient"] == ingredient:
                element["weight"] = str(float(element["weight"]) + float(weight))
        file = open("inventory.csv","w")
        fieldnames = ["name", "zip", "ingredient", "weight"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)
        file.close()
    else:
        file = open("inventory.csv", "a")
        writer = csv.DictWriter(file, fieldnames=["name","zip","ingredient","weight"])
        writer.writerow({"name":shop.name,"zip":shop.zip,"ingredient":ingredient,"weight":weight})
        file.close()

    #Changing the investment of the shop due to the recent purchase
    shop.investment = str(float(shop.investment) + float(price))
    file = open("stores.csv", "r")
    reader = csv.DictReader(file)
    data = []
    for row in reader:
        data.append(row)

    for element in data:
        if element["name"] == shop.name and element["zip"] == shop.zip:
            element["investment"] = shop.investment
    file.close()

    file = open("stores.csv", "w")
    writer = csv.DictWriter(file, fieldnames=["name","zip","investment","total_revenue"])
    writer.writeheader()
    writer.writerows(data)
    file.close()



def sell(shop):
    #Getting the product that is to be sold
    print("Choose among expresso, mocha, cappuccino or latte")
    while True:
        type = input("Enter type of coffee: ").lower()
        check = isvalid(type)
        if check == True:
            break

    #Adjusting the proportion of ingredient based on the product chosen to be sold
    milk = 0
    sugar = 0
    chocolate = 0
    if type == "expresso":
        coffee = 0.02
        price = 2.5
    elif type == "mocha":
        milk = 0.15
        chocolate = 0.01
        coffee = 0.02
        sugar = 0.015
        price = 5.0
    elif type == "latte":
        sugar = 0.01
        milk = 0.15
        coffee = 0.025
        price = 3.5
    else:
        milk = 0.12
        coffee = 0.02
        price = 4.5

    #Changing the profit of the shop as a product is sold
    shop.total_revenue = str(float(shop.total_revenue) + price)
    file = open("stores.csv", "r")
    reader = csv.DictReader(file)
    data = []
    for row in reader:
        data.append(row)

    for element in data:
        if element["name"] == shop.name and element["zip"] == shop.zip:
            element["total_revenue"] = shop.total_revenue
    file.close()

    file = open("stores.csv", "w")
    writer = csv.DictWriter(file, fieldnames=["name","zip","investment","total_revenue"])
    writer.writeheader()
    writer.writerows(data)
    file.close()

    #Decreasing the weight of the ingredients used to make the product
    file = open("inventory.csv","r")
    reader = csv.DictReader(file)
    items = []
    count = 0
    for row in reader:
        items.append(row)
        if row["name"] == shop.name and row["zip"] == shop.zip:
            if row["ingredient"] == "milk":
                if float(row["weight"]) < milk:
                    sys.exit("Not enough ingredients in inventory")
                else:
                    count = count + 1
            elif row["ingredient"] == "sugar":
                if float(row["weight"]) < sugar:
                    sys.exit("Not enough ingredients in inventory")
                else:
                    count = count + 1
            elif row["ingredient"] == "coffee":
                if float(row["weight"]) < coffee:
                    sys.exit("Not enough ingredients in inventory")
                else:
                    count = count + 1
            elif row["ingredient"] == "chocolate":
                if float(row["weight"]) < chocolate:
                    sys.exit("Not enough ingredients in inventory")
                else:
                    count = count + 1
    if count != 4:
        sys.exit("Not enough ingredients in inventory")
    file.close()

    for element in items:
        if element["name"] == shop.name and element["zip"] == shop.zip:
            if element["ingredient"] == "milk":
                element["weight"] = str(float(element["weight"]) - milk)
            elif element["ingredient"] == "coffee":
                element["weight"] = str(float(element["weight"]) - coffee)
            elif element["ingredient"] == "chocolate":
                element["weight"] = str(float(element["weight"]) - chocolate)
            elif element["ingredient"] == "sugar":
                element["weight"] = str(float(element["weight"]) - sugar)

    file = open("inventory.csv","w")
    fieldnames = ["name", "zip", "ingredient", "weight"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(items)
    file.close()

    #Adding the details of the recently sold product to the file
    file = open("sells.csv","a")
    fieldnames = ["name", "zip", "item", "price"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writerow({"name":shop.name,"zip":shop.zip,"item":type,"price":price})
    file.close()


def isvalid(type):
    #Function to check whether product is being sold by shop or not
    if type.lower() in ["expresso","mocha","cappuccino","latte"]:
        return True
    else:
        return False


def storage(shop):
    #Reading the details of the ingredients from the file and then printing the details of the ingredients
    print()
    file = open("inventory.csv", "r")
    reader = csv.DictReader(file)
    for row in reader:
        if row["name"] == shop.name and row["zip"] == shop.zip:
            if row["ingredient"] == "milk":
                print(f'{row["ingredient"].capitalize()}: {row["weight"]}litre')
            else:
                print(f'{row["ingredient"].capitalize()}: {row["weight"]}kg')


def profit(shop):
    #Providing total profit made by the shop
    profit = float(shop.total_revenue) - float(shop.investment)
    print(f"{shop.name.capitalize()} with zipcode: {shop.zip} has total profit of ${profit}")


if __name__ == "__main__":
    main()