"""
############################################
# Restaurant POS with Stock Control System #
# Wasim Ahmed - Kings School Grantham      #
############################################
"""
# PYTHON 3.9
# IMPORT PACKAGE / PYTHON FILES
import sys
import csv
import os.path
import hashlib
import sqlite3 as sql
import matplotlib.pyplot as plt
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from datetime import datetime
from Splash import Ui_SplashScreen
from Login import Ui_frmLogin
from Home import Ui_frmHome
from Menu import Ui_frmMenu
from Ingredients import Ui_frmIngredients
from TakeOrder import Ui_frmTakeOrder
from KitchenView import Ui_frmKitchenView
from Suppliers import Ui_frmSuppliers
from StockReplenishment import Ui_frmStockReplenishment

# DB INITIALIZATION
conn = sql.connect('ACCOUNTS.db')
command = conn.cursor()   # Execute commands on Authentication DB

conn_2 = sql.connect('POS.db')
command_2 = conn_2.cursor()  # Execute commands on System DB

# GLOBAL VARIABLES
COUNTER = 0  # Progress Bar - Splash Screen
USER_ROLE = ""  # Stores Users Role in business - Whole program
USERNAME = ""  # Stores Username of worker - Whole Program
NUM_PRESENT_M = False  # Boolean for num validation - Menu Form
CHAR_PRESENT_M = False  # Boolean for char validation - Menu Form
EDITED_RECORD = False  # Boolean for updating record - Menu Form
NUM_PRESENT_I = False  # Boolean for num validation - Ingred Form
CHAR_PRESENT_I = False  # Boolean for char validation - Ingred Form
EDITED_MEAL_ITEM_ID = 0  # For storing updated meal record ID from SQL output - Menu Form
ORDER_ID = 0  # Stores id which increments with orders - Take Order Form
FOUND = False  # Boolean for finding matching order num in txt file in loop - Kitchen View Form


class SplashScreen(QMainWindow, Ui_SplashScreen):
    def __init__(self):  # CONSTRUCTOR METHOD
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(980, 500)

        # Remove Title Bar
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set timer for progress bar
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)

    def progress(self):  # PROGRESS BAR
        global COUNTER
        self.prgbar.setValue(COUNTER)
        if COUNTER > 100:
            self.timer.stop()
            login = LoginWin()
            widget.addWidget(login)
            widget.show()
            self.close()
        else:
            COUNTER += 1


class LoginWin(QMainWindow, Ui_frmLogin):
    def __init__(self):  # CONSTRUCTOR METHOD
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(345, 396)
        self.btnLogin.clicked.connect(self.login)
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def login(self):  # LOGIN METHOD
        # Get username from textbox then validate against db
        command.execute(f"SELECT * FROM USERS WHERE USERNAME = '{self.txtUsername.text()}'")
        user_exists = command.fetchall()
        if not user_exists:
            msg = QMessageBox()
            msg.setWindowTitle("LOGIN UNSUCCESSFUL")
            msg.setText("Login not found!")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
            self.txtUsername.clear()
            self.txtPassword.clear()
            self.txtUsername.setFocus()
        else:  # Compare hashed password from db to hashed password of user input
            actual_password = [col[3] for col in user_exists]
            sh = hashlib.sha1()
            sh.update(self.txtPassword.text().encode('utf-8'))
            hashed_password = sh.hexdigest()
            if hashed_password == actual_password[0]:
                global USERNAME
                USERNAME = self.txtUsername.text()
                command.execute(f"SELECT ROLE FROM USERS WHERE USERNAME = '{USERNAME}'")
                global USER_ROLE
                USER_ROLE = str(command.fetchone()).strip("(',')")
                home = Home()
                widget.addWidget(home)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                self.close()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("LOGIN UNSUCCESSFUL")
                msg.setText("Login not found!")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec()
                self.txtUsername.clear()
                self.txtPassword.clear()
                self.txtUsername.setFocus()


class Home(QMainWindow, Ui_frmHome):
    def __init__(self):  # CONSTRUCTOR METHOD
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(980, 500)
        self.lblUsername.setText(USERNAME)
        self.btnMenu.clicked.connect(self.menu)
        self.btnIngredients.clicked.connect(self.ingredients)
        self.btnOrder.clicked.connect(self.takeorder)
        self.btnKitchen.clicked.connect(self.kitchen)
        self.btnSuppliers.clicked.connect(self.suppliers)
        self.btnStockReplenishment.clicked.connect(self.stockreplenishment)
        self.btnPopularProd.clicked.connect(self.popularprod)

        # Set all buttons to 'not enabled' by default
        self.btnMenu.setEnabled(False)
        self.btnIngredients.setEnabled(False)
        self.btnOrder.setEnabled(False)
        self.btnKitchen.setEnabled(False)
        self.btnSuppliers.setEnabled(False)
        self.btnStockReplenishment.setEnabled(False)
        self.btnPopularProd.setEnabled(False)

        # Assign access control
        if USER_ROLE == "WT":  # Waiter
            self.btnOrder.setEnabled(True)
        elif USER_ROLE == "CR":  # Cashier
            self.btnOrder.setEnabled(True)
        elif USER_ROLE == "KT":  # Kitchen Staff
            self.btnKitchen.setEnabled(True)
        elif USER_ROLE == "HC":  # Head Chef
            self.btnMenu.setEnabled(True)
            self.btnIngredients.setEnabled(True)
            self.btnKitchen.setEnabled(True)
        elif USER_ROLE == "MA":  # Manager
            self.btnMenu.setEnabled(True)
            self.btnIngredients.setEnabled(True)
            self.btnOrder.setEnabled(True)
            self.btnKitchen.setEnabled(True)
            self.btnSuppliers.setEnabled(True)
            self.btnStockReplenishment.setEnabled(True)
            self.btnPopularProd.setEnabled(True)

    def menu(self):  # GO TO MENU WINDOW
        menuwin = MenuWin()
        widget.addWidget(menuwin)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    def ingredients(self):  # GO TO INGREDIENTS WINDOW
        ingredwin = IngredientsWin()
        widget.addWidget(ingredwin)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    def takeorder(self):  # GO TO TAKE ORDER WINDOW
        orderwin = TakeOrderWin()
        widget.addWidget(orderwin)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    def kitchen(self):  # GO TO KITCHEN WINDOW
        kitchen = KitchenViewWin()
        widget.addWidget(kitchen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    def suppliers(self):  # GO TO SUPPLIERS WINDOW
        suppliers = SuppliersWin()
        widget.addWidget(suppliers)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    def stockreplenishment(self):  # GO TO STOCK REPLENISHMENT WINDOW
        stockreplenishment = StockReplenishmentWin()
        widget.addWidget(stockreplenishment)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    @staticmethod
    def popularprod():  # GET DATA FOR POPULAR PRODUCTS GRAPH
        # Populate the Orders array from text file
        orders = []
        order_file = open('orders.txt', 'r')
        for line in order_file:
            orders.append(line)

        # Create an array of each element inside this array - so a double array e.g --> [['a', 'b'], ['c', ''d]]
        orders = list(csv.reader(orders))

        # Loop through each order (a line in the text file) + remove last 2 elements and first element
        for order in orders:
            del order[len(order) - 2:]
            del order[0]

        # Remove white spaces in each element of an order
        orders = [element.strip(' ') for order in orders for element in order]

        # Tally the food items and store names, quantities separately
        Food_items = []
        Quantities = []

        for i in range(0, len(orders) - 1):
            string = orders[i].split("x", 1)
            quantity = int(string[0].strip())
            food_item = string[1].strip()
            exists = food_item in Food_items
            if exists:
                continue
            else:
                for j in range(i + 1, len(orders) - 1):
                    string_2 = orders[j].split("x", 1)
                    quantity_2 = int(string_2[0].strip())
                    food_item_2 = string_2[1].strip()
                    if food_item == food_item_2:
                        quantity += quantity_2
                Food_items.append(food_item)
                Quantities.append(quantity)

        # Graph the data
        plt.figure(num="ALATURKA")
        plt.bar(Food_items, Quantities)
        plt.title('Popular Foods Sold')
        plt.xlabel('Food Items')
        plt.xticks(fontsize=6)
        plt.ylabel('Quantities')
        plt.show()


class MenuWin(QMainWindow, Ui_frmMenu):
    def __init__(self):  # CONSTRUCTOR METHOD
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(980, 500)
        self.lblUsername.setText(USERNAME)
        self.btnBack.clicked.connect(self.back)
        self.btnEdit.clicked.connect(self.edit)
        self.btnSave.clicked.connect(self.save)
        self.btnDelete.clicked.connect(self.delete)
        self.cmbMealType.addItem('Starter')
        self.cmbMealType.addItem('Main Course')
        self.cmbMealType.addItem('Dessert')
        self.cmbMealType.addItem('Beverage')
        self.ingredientsview()
        self.refresh_listbox()

    def ingredientsview(self):  # PULLS INGREDIENT NAMES FROM INGREDIENTS TABLE + POPULATES LIST BOX
        self.lstIngredientsView.clear()
        command_2.execute("SELECT NAME FROM INGREDIENTS")
        record = command_2.fetchall()
        for rec in record:
            self.lstIngredientsView.addItem(str(rec).strip("('',)"))

    def refresh_listbox(self):  # PULLS CERTAIN DATA FROM MENU TABLE + POPULATES LIST BOX
        self.lstMenuView.clear()
        command_2.execute("SELECT * FROM MENU")
        records = command_2.fetchall()
        for record in records:
            self.lstMenuView.addItem(record[1][0] + " - " + record[2] + " - " + str(record[4]))

    def back(self):  # GOES BACK TO HOME WINDOW
        self.lstIngredientsView.clearSelection()
        home = Home()
        self.setFixedSize(980, 500)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    def edit(self):  # EDIT A MEAL
        self.txtName.clear()
        self.txtDesc.clear()
        self.txtPrice.clear()
        self.lstIngredientsView.clearSelection()

        item_to_edit = self.lstMenuView.currentItem().text()
        meal_name = (item_to_edit[4:])[:-7]

        command_2.execute(f"SELECT * FROM MENU WHERE NAME='{meal_name}'")
        meal_record = command_2.fetchall()[0]

        global EDITED_MEAL_ITEM_ID

        EDITED_MEAL_ITEM_ID, meal_type, meal_name, meal_desc, meal_price = [meal_record[i] for i in range(
            0, len(meal_record))]

        self.cmbMealType.setCurrentText(meal_type)
        self.txtName.setText(meal_name)
        self.txtDesc.setText(meal_desc)
        self.txtPrice.setText(str(meal_price))

        # Get all current ingredient names for that meal item
        command_2.execute(f"SELECT IngredientID FROM MENUINGREDIENTS WHERE MenuID='{EDITED_MEAL_ITEM_ID}'")
        ingredient_ids = command_2.fetchall()
        preselect_ingred_names = []
        for ingredient_id in ingredient_ids:
            command_2.execute("SELECT Name FROM INGREDIENTS WHERE IngredientID='%s'" % ingredient_id)
            ingred_name = str(command_2.fetchone()).strip("('',)")
            preselect_ingred_names.append(ingred_name)

        # Highlights the current ingredients in the list for the user
        for x in range(0, self.lstIngredientsView.count()):
            for y in range(0, len(preselect_ingred_names)):
                if self.lstIngredientsView.item(x).text() == preselect_ingred_names[y]:
                    self.lstIngredientsView.item(x).setSelected(True)
                    break

        global EDITED_RECORD
        EDITED_RECORD = True

    def save(self):  # SAVES TO DB + DISPLAYS / UPDATES LIST BOX
        # Check if 'MENU' table exists
        command_2.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MENU'")
        if command_2.fetchone()[0] != 'MENU':
            query = ('''
                    CREATE TABLE MENU 
                    (MenuID integer PRIMARY KEY, 
                    Type tinytext, 
                    Name tinytext, 
                    Description varchar(35), 
                    MealPrice decimal(2, 2))
            ''')
            command_2.execute(query)
            conn_2.commit()

        menu_type = self.cmbMealType.currentText()
        meal_name = self.txtName.text()
        meal_desc = self.txtDesc.text()
        meal_price = self.txtPrice.text()

        # Validation for Name, Price Fields + Updates table based on any edits
        global NUM_PRESENT_M
        global CHAR_PRESENT_M
        NUM_PRESENT_M = any(map(str.isdigit, meal_name))  # Boolean value
        CHAR_PRESENT_M = any(map(str.isalpha, meal_price))  # Boolean value

        global EDITED_RECORD

        if not [x for x in (menu_type, meal_name, meal_desc, meal_price) if x == ""]:  # If not empty
            if NUM_PRESENT_M:  # If num present in 'name' field
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText("Enter only LETTERS in NAME field")
                msg.exec()
            else:
                if CHAR_PRESENT_M:  # If letter present in 'price' field
                    msg = QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("Enter only NUMBERS in PRICE field")
                    msg.exec()
                else:
                    if menu_type == "Beverage":
                        if EDITED_RECORD:  # Record been edited
                            command_2.execute(f"SELECT MenuID FROM MENU WHERE Name='{meal_name}'")
                            updated_bev_id = str(command_2.fetchone()).strip("(,)")

                            query = ('''
                                        UPDATE MENU SET Type=?, Name=?, Description=?, MealPrice=? WHERE MenuID=?
                                     ''')

                            command_2.execute(query, (menu_type, meal_name, meal_desc, meal_price, updated_bev_id))
                            conn_2.commit()
                            EDITED_RECORD = False

                            self.txtName.clear()
                            self.txtDesc.clear()
                            self.txtPrice.clear()

                            msg = QMessageBox()
                            msg.setWindowTitle("SUCCESS")
                            msg.setText("Drink successfully UPDATED in menu")
                            msg.exec()

                            self.ingredientsview()
                            self.refresh_listbox()

                        elif not EDITED_RECORD:  # Record not edited
                            query = ('''
                                        INSERT INTO MENU (Type, Name, Description, MealPrice) VALUES (?, ?, ?, ?)
                                    ''')
                            command_2.execute(query, (menu_type, meal_name, meal_desc, meal_price))
                            conn_2.commit()

                            self.txtName.clear()
                            self.txtDesc.clear()
                            self.txtPrice.clear()

                            msg = QMessageBox()
                            msg.setWindowTitle("SUCCESS")
                            msg.setText("Drink ADDED successfully to menu")
                            msg.exec()

                            self.ingredientsview()
                            self.refresh_listbox()

                    elif self.lstIngredientsView.currentItem() is not None:  # All validation passed
                        if EDITED_RECORD:  # Record been edited
                            query = ('''
                                         UPDATE MENU SET Type=?, Name=?, Description=?, MealPrice=?
                                         WHERE MenuID=?
                                     ''')
                            command_2.execute(query, (menu_type, meal_name, meal_desc, meal_price, EDITED_MEAL_ITEM_ID))
                            conn_2.commit()

                            ingreds = []  # Populate with newly selected ingreds from listbox
                            ingred_ids = []  # SQL in For-Loop populates with ID's for ingredient in 'ingreds'
                            [ingreds.append(str(item.text())) for item in self.lstIngredientsView.selectedItems()]

                            # Gets ingredient id from their names in 'ingreds' + stores in array 'ingred_ids'
                            for x in range(0, len(ingreds)):
                                command_2.execute(f"SELECT IngredientID FROM INGREDIENTS WHERE Name='{ingreds[x]}'")
                                ingred_ids.append(str(command_2.fetchone()).strip("(,)"))

                            # Gets primary key value from Link-Table + Store in array
                            query = f"SELECT MenuIngID FROM MENUINGREDIENTS WHERE MenuID='{EDITED_MEAL_ITEM_ID}'"
                            command_2.execute(query)
                            p_keys_sql = []
                            for p_key in command_2.fetchall():
                                p_keys_sql.append(str(p_key).strip("('',)"))

                            # Loop through primary keys + For each primary key, update ingredient id in link table
                            # With new ingredient id from 'ingred_ids'
                            for x, y in zip(ingred_ids, p_keys_sql):
                                query = ("UPDATE MENUINGREDIENTS SET IngredientID={0} where MenuIngID={1}".format(x, y))
                                command_2.execute(query)
                            conn_2.commit()
                            EDITED_RECORD = False

                            msg = QMessageBox()
                            msg.setWindowTitle("SAVED")
                            msg.setText("Menu item SUCCESSFULLY updated!")
                            msg.exec()

                            self.txtName.clear()
                            self.txtDesc.clear()
                            self.txtPrice.clear()
                            self.lstIngredientsView.clearSelection()
                            self.refresh_listbox()

                        elif not EDITED_RECORD:  # Record not edited
                            query = ('''
                                        INSERT INTO MENU (Type, Name, Description, MealPrice) VALUES (?, ?, ?, ?)
                                     ''')
                            command_2.execute(query, (menu_type, meal_name, meal_desc, meal_price))
                            conn_2.commit()

                            # New record for new menu option in link table + stores 'MenuID' + 'IngredientID' with it
                            ingredients = []
                            [ingredients.append(str(item.text())) for item in self.lstIngredientsView.selectedItems()]

                            command_2.execute(f"SELECT MenuID FROM MENU WHERE Name='{meal_name}'")
                            menu_id = str(command_2.fetchone()).strip("(,)")

                            for i in range(0, len(ingredients)):
                                command_2.execute(f"SELECT IngredientID FROM INGREDIENTS WHERE Name='{ingredients[i]}'")
                                ingredient_id = str(command_2.fetchone()).strip("(,)")
                                query = "INSERT INTO MENUINGREDIENTS (IngredientID, MenuID) VALUES (?, ?)"
                                command_2.execute(query, (ingredient_id, menu_id))
                                conn_2.commit()

                            self.txtName.clear()
                            self.txtDesc.clear()
                            self.txtPrice.clear()

                            msg = QMessageBox()
                            msg.setWindowTitle("SUCCESS")
                            msg.setText("Meal ADDED successfully to menu")
                            msg.exec()

                            self.ingredientsview()
                            self.refresh_listbox()

                    else:
                        msg = QMessageBox()
                        msg.setWindowTitle("ERROR")
                        msg.setText("Select INGREDIENTS needed for the meal")
                        msg.exec()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("Enter ALL values")
            msg.exec()

    def delete(self):  # DELETES RECORD FROM 'MENU' TABLE + ADJUSTS LINK-TABLE ACCORDINGLY
        selected_item = self.lstMenuView.currentItem().text()[4:]
        delimiter = " -"
        meal_name = selected_item.split(delimiter, 1)[0]
        command_2.execute(f"SELECT MenuID FROM MENU WHERE Name='{meal_name}'")
        meal_id = str(command_2.fetchone()).strip("(,)")
        try:
            command_2.execute(f"DELETE FROM MENU WHERE NAME='{meal_name}'")
            conn_2.commit()
            command_2.execute(f"DELETE FROM MENUINGREDIENTS WHERE MenuID='{meal_id}'")
            conn_2.commit()
            msg = QMessageBox()
            msg.setWindowTitle("SUCCESS")
            msg.setText("Item DELETED successfully from menu")
            msg.exec()
            self.refresh_listbox()
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("Item HASN'T been deleted. Please try again")
            msg.exec()
            self.refresh_listbox()


class IngredientsWin(QMainWindow, Ui_frmIngredients):
    def __init__(self):  # CONSTRUCTOR METHOD
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(980, 500)
        self.lblUsername.setText(USERNAME)
        self.btnBack.clicked.connect(self.back)
        self.btnSave.clicked.connect(self.save)
        self.btnDelete.clicked.connect(self.delete)
        self.refresh_listbox()

    def refresh_listbox(self):  # PULLS DATA FROM INGREDIENTS TABLE + POPULATES LIST BOX
        self.lstIngredientView.clear()
        command_2.execute("SELECT * FROM INGREDIENTS")
        records = command_2.fetchall()
        for record in records:
            self.lstIngredientView.addItem(record[1] + " - " + str(record[2]))

    def back(self):  # GOES BACK TO HOME WINDOW
        home = Home()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    def save(self):  # SAVES TO DB + DISPLAYS / UPDATES LIST BOX
        # Check if 'INGREDIENTS' table exists
        command_2.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='INGREDIENTS'")
        if command_2.fetchone()[0] != 'INGREDIENTS':
            query = ('''
                            CREATE TABLE INGREDIENTS 
                            (IngredientID integer PRIMARY KEY, 
                            Name tinytext, 
                            Quantity varchar(20), 
                            CostPrice decimal(2, 2))
                            MinOrderLvl varchar(20)
                    ''')
            command_2.execute(query)
            conn_2.commit()

        ingred_name = self.txtName.text()
        ingred_quantity = self.txtQuantity.text()
        ingred_cprice = self.txtCostPrice.text()
        ingred_minlvl = self.txtMinOrderLvl.text()

        # Validation for Name, Quantity, Cost Price fields
        global NUM_PRESENT_I
        NUM_PRESENT_I = any(map(str.isdigit, ingred_name))

        if not [x for x in (ingred_name, ingred_quantity, ingred_cprice, ingred_minlvl) if x == ""]:  # If not empty
            if NUM_PRESENT_I:  # If num present in 'name' field
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText("Enter only LETTERS in NAME field")
                msg.exec()
            else:  # if num not present in field
                query = ('''
                            INSERT INTO INGREDIENTS (Name, Quantity, CostPrice, MinOrderLvl) VALUES (?, ?, ?, ?)
                        ''')
                command_2.execute(query, (ingred_name, ingred_quantity, ingred_cprice, ingred_minlvl))
                conn_2.commit()
                self.txtName.clear()
                self.txtQuantity.clear()
                self.txtCostPrice.clear()
                self.txtMinOrderLvl.clear()
                msg = QMessageBox()
                msg.setWindowTitle("SUCCESS")
                msg.setText("Ingredient ADDED successfully to pantry")
                msg.exec()
                self.refresh_listbox()

        else:  # Fields are empty
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("Enter ALL values")
            msg.exec()

    def delete(self):  # DELETES RECORD FROM 'INGREDIENTS' TABLE
        if self.lstIngredientView.currentItem() is not None:
            selected_item = self.lstIngredientView.currentItem().text().strip(" -")
            delimiter = " -"
            ingredient = selected_item.split(delimiter, 1)[0]
            query = "DELETE FROM INGREDIENTS WHERE NAME='" + ingredient + "'"
            try:
                command_2.execute(query)
                conn_2.commit()
                msg = QMessageBox()
                msg.setWindowTitle("SUCCESS")
                msg.setText("Item DELETED successfully from menu")
                msg.exec()
                self.refresh_listbox()
            except ValueError:
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText("Item HASN'T been deleted. Please try again")
                msg.exec()
                self.refresh_listbox()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("SELECT item from list to delete.")
            msg.exec()


class TakeOrderWin(QMainWindow, Ui_frmTakeOrder):
    def __init__(self):  # CONSTRUCTOR METHOD
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(980, 500)
        self.lblUsername.setText(USERNAME)
        self.btnBack.clicked.connect(self.back)
        self.btnAdd.clicked.connect(self.add)
        self.btnDelete.clicked.connect(self.delete)
        self.btnSave.clicked.connect(self.save)
        self.btnClear.clicked.connect(self.clear)
        self.populate_cmb()

    def populate_cmb(self):  # POPULATES COMBO BOX ON FORM LOAD
        command_2.execute("SELECT NAME FROM MENU")
        meal_names = command_2.fetchall()
        for item in range(0, len(meal_names)):
            self.cmbOrderName.addItem(str(meal_names[item]).strip("(',)')"))

    def back(self):  # GOES BACK TO HOME WINDOW
        home = Home()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    def add(self):  # ADD ORDER TO LIST BOX
        Meal_Name = self.cmbOrderName.currentText()
        Quantity = self.spnQuantity.text()
        if Quantity == "0":  # Validation Check
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("No Quantity was added! Please choose a quantity.")
            msg.exec()
        else:  # Adds record to list box
            quantity_mealname = str(Quantity + " x " + Meal_Name)
            self.lstOrderView.addItem(quantity_mealname)
            self.cmbOrderName.setCurrentText("")
            self.spnQuantity.setValue(0)

    def delete(self):  # REMOVE ORDER FROM LIST BOX
        entries_from_list = []
        if self.lstOrderView.currentItem() is not None:
            for item in range(0, self.lstOrderView.count()):  # Copy current list box contents to new array
                entries_from_list.append(self.lstOrderView.item(item).text())

            for item in range(0, len(entries_from_list)):  # Remove selected item from new array
                if entries_from_list[item] == self.lstOrderView.currentItem().text():
                    entries_from_list.pop(item)
                    break

            self.lstOrderView.clear()  # Clear the list box

            for item in range(0, len(entries_from_list)):  # Copy new array contents to list box
                self.lstOrderView.addItem(entries_from_list[item])

            msg = QMessageBox()
            msg.setWindowTitle("SUCCESS")
            msg.setText("Entry REMOVED from order.")
            msg.exec()

        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("SELECT entry from order to delete.")
            msg.exec()

    def clear(self):  # CLEAR THE LIST BOX
        self.lstOrderView.clear()

    def save(self):  # SAVE ORDER TO FILE + SHOW 'RECEIPT'
        global ORDER_ID
        # Store the order as a string for receipt + get food items to validate stock levels
        orders = ''''''
        Food_Items = []
        for entry in range(0, self.lstOrderView.count()):
            string = self.lstOrderView.item(entry).text().split("x", 1)
            Food_Items.append(string[1].strip())
            orders += self.lstOrderView.item(entry).text() + ", "

        isStock = False

        # Get Food Item ID, Type from Menu table
        for item in Food_Items:
            command_2.execute("SELECT MenuID,Type FROM MENU WHERE Name='%s'" % item)
            result = command_2.fetchall()
            food_id, food_type = result[0]
            if food_type == "Beverage":  # Ignore items where type = beverage
                continue
            else:  # Get all ingred id's related to that food item(meal)
                ingred_ids = []
                command_2.execute("SELECT IngredientID FROM MENUINGREDIENTS WHERE MenuID=%s" % food_id)
                results = command_2.fetchall()
                for x in results:
                    ingred_ids.append(str(x).strip("(,)"))
                for i_id in ingred_ids:  # Loop through each of the ingredient ID's
                    command_2.execute("SELECT Quantity,MinOrderLvl FROM INGREDIENTS WHERE IngredientID='%s'" % i_id)
                    results = command_2.fetchall()

                    raw_quantity, raw_minorderlvl = results[0]
                    quantity_filter = filter(str.isdigit, raw_quantity)
                    quantity = int("".join(quantity_filter).strip())

                    minorderlvl_filter = filter(str.isdigit, raw_minorderlvl)
                    minorderlvl = int("".join(minorderlvl_filter).strip())

                    isStock = quantity > minorderlvl

                    command_2.execute("SELECT Name FROM INGREDIENTS WHERE IngredientID='%s'" % i_id)
                    name = str(command_2.fetchone()).strip("(',)")

                    if not isStock:  # Not in stock then write to file and break loop
                        if os.path.isfile("stock_replenishment.txt"):  # If file exists
                            file = open('stock_replenishment.txt', 'r')
                            contents = file.read()
                            if name in contents:  # If name already in the file then skip
                                pass
                            else:
                                file.close()
                                file = open('stock_replenishment.txt', 'a')
                                file.write(name + "\n")
                                break
                        else:  # Else file doesn't exist
                            with open('stock_replenishment.txt', 'a') as f:
                                f.write(name + "\n")
                            break

            if not isStock:  # If not in stock, show meal that can't be made, then break loop
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText(f"{item} meal not available")
                self.lstOrderView.clear()
                msg.exec()
                break

        if isStock:  # If every meal is in stock then save and show receipt
            if os.path.isfile("orders.txt"):  # If file exist
                # Store New Order Num -> Get current order num from eof file and + 1
                orders_file = open("orders.txt", "rt")
                lineList = orders_file.readlines()
                orders_file.close()
                ORDER_ID = int((lineList[-1:][0]).split(",")[0]) + 1

                # Get the full name of the user
                command.execute("SELECT FNAME,LNAME FROM USERS WHERE USERNAME='%s'" % USERNAME)
                result = command.fetchall()
                first_name = result[0][0]
                last_name = result[0][1]
                full_name = first_name + " " + last_name

                # Get system date + time
                now = datetime.now()
                date_time = now.strftime("%d/%m/%Y %H:%M")

                # Store order in file -> Format with order num + order
                orders_file = open("orders.txt", "at")
                orders_file.write("\n" + str(ORDER_ID) + ", " + orders + full_name + ", " + date_time)
                orders_file.close()

                msg = QMessageBox()
                msg.setWindowTitle("SUCCESS")
                msg.setText("Order SAVED + SENT to kitchen")
                msg.exec()

                # Display the order in the format of a receipt
                msg = QMessageBox()
                orders = ''''''
                for entry in range(0, self.lstOrderView.count()):
                    orders += self.lstOrderView.item(entry).text() + "\n"

                msg.setWindowTitle("View Receipt")
                msg.setText("Order ID - " + str(ORDER_ID) + "\n" + orders + "\n" + full_name + "\n" + date_time)
                msg.exec()

                self.lstOrderView.clear()

            else:  # Else file doesn't exist -> Same code as above except 'Order_id' = 1 for first order
                ORDER_ID += 1

                command.execute("SELECT FNAME,LNAME FROM USERS WHERE USERNAME='%s'" % USERNAME)
                result = command.fetchall()
                first_name = result[0][0]
                last_name = result[0][1]
                full_name = first_name + " " + last_name

                now = datetime.now()
                date_time = now.strftime("%d/%m/%Y %H:%M")

                orders_file = open("orders.txt", "at")
                orders = ''''''
                for entry in range(0, self.lstOrderView.count()):
                    orders += self.lstOrderView.item(entry).text() + ", "

                orders_file.write(str(ORDER_ID) + ", " + orders + full_name + ", " + date_time)
                orders_file.close()

                msg = QMessageBox()
                msg.setWindowTitle("SUCCESS")
                msg.setText("Order SAVED + SENT to kitchen")
                msg.exec()

                msg = QMessageBox()
                orders = ''''''
                for entry in range(0, self.lstOrderView.count()):
                    orders += self.lstOrderView.item(entry).text() + "\n"

                msg.setWindowTitle("View Receipt")
                msg.setText("Order ID - " + str(ORDER_ID) + "\n" + orders + "\n" + full_name + "\n" + date_time)
                msg.exec()

                self.lstOrderView.clear()


class KitchenViewWin(QMainWindow, Ui_frmKitchenView):
    def __init__(self):  # CONSTRUCTOR METHOD
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(980, 500)
        self.lblUsername.setText(USERNAME)
        self.btnBack.clicked.connect(self.back)
        self.btnComplete.clicked.connect(self.completed)
        self.btnRefresh.clicked.connect(self.refresh)
        self.refresh()

    def refresh(self):  # UPDATES LIST BOX WITH ORDERS MADE ON SYSTEM DAY
        self.lstOrderView.clear()
        orders_file = open("orders.txt", "rt")

        # Add dates, order num from each entry in txt file
        Dates = []
        for entry in orders_file:
            order = entry.split(", ")
            Dates.append(order[-1] + "," + order[0])
        orders_file.close()

        # Bubble sort Dates array
        for x in range(len(Dates)):
            swapped = False
            i = 0
            while i < len(Dates) - 1:
                if Dates[i + 1] > Dates[i]:
                    # Swap Values
                    Dates[i], Dates[i + 1] = Dates[i + 1], Dates[i]
                    swapped = True
                i = i + 1

            if not swapped:
                break

        # Compares sorted dates to the system date - if match store order num in another array
        today_order_nums = []
        now = datetime.now()
        system_date = now.strftime("%d/%m/%Y")
        for date in Dates:
            if date[:10] == system_date:
                split = date.split(",")
                today_order_nums.append(split[1])

        # Compare order num of each entry in file, to order num in array
        orders_file = open("orders.txt", "rt")
        today_order_nums.reverse()
        self.lstOrderView.setSpacing(5)
        for entry in orders_file:
            order = entry.split(", ")
            for x in range(0, len(today_order_nums)):
                if order[0] == today_order_nums[x]:
                    string = ""
                    for y in range(1, len(order) - 2):
                        string += order[y] + ","
                    print("Order Number - " + today_order_nums[x] + " , " + string[:-1])
                    self.lstOrderView.addItem("Order Number - " + today_order_nums[x] + " ," + string[:-1])
                elif order[0] < today_order_nums[x]:
                    break
        orders_file.close()

    def back(self):  # GOES BACK TO HOME WINDOW
        home = Home()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    def completed(self):  # REMOVES ORDER FROM LIST BOX
        orders_from_list = []
        if self.lstOrderView.currentItem() is not None:
            for item in range(0, self.lstOrderView.count()):
                orders_from_list.append(self.lstOrderView.item(item).text())

            for order in range(0, len(orders_from_list)):
                if orders_from_list[order] == self.lstOrderView.currentItem().text():
                    orders_from_list.pop(order)
                    break

            self.lstOrderView.clear()

            for order in range(0, len(orders_from_list)):
                self.lstOrderView.addItem(orders_from_list[order])


class SuppliersWin(QMainWindow, Ui_frmSuppliers):
    def __init__(self):  # CONSTRUCTOR METHOD
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(980, 500)
        self.lblUsername.setText(USERNAME)
        self.btnFind.clicked.connect(self.find_name)
        self.btnEdit.clicked.connect(self.edit)
        self.btnSave.clicked.connect(self.save)
        self.btnDelete.clicked.connect(self.delete)
        self.btnBack.clicked.connect(self.back)
        self.btnEdit.setVisible(False)
        self.btnDelete.setVisible(False)

    def find_name(self):  # SEARCH SUPPLIER CONTACTS
        supplier_name = self.txtFindName.text()
        if supplier_name != "":  # Validation check for empty string
            command_2.execute(f"SELECT * FROM SUPPLIERS WHERE Name='{supplier_name}'")
            try:  # If record exists - show info in respective fields
                result = command_2.fetchall()[0]
                supplier_id, supplier_name, supplier_address, supplier_telephone = [result[i] for i in range(
                    0, len(result))]
                self.txtName.setText(supplier_name)
                self.txtAddress.setText(supplier_address)
                self.txtPhone.setText(supplier_telephone)

                self.txtName.setEnabled(False)
                self.txtAddress.setEnabled(False)
                self.txtPhone.setEnabled(False)

                self.txtFindName.clear()
                self.btnEdit.setVisible(True)
                self.btnDelete.setVisible(True)
                self.btnSave.setVisible(False)

            except IndexError:  # Else record doesn't exist
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText("Record DOES NOT exist.")
                msg.exec()
                self.txtFindName.clear()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("Enter the NAME of the supplier.")
            msg.exec()

    def edit(self):  # EDIT SUPPLIER CONTACT INFO
        self.txtName.setEnabled(True)
        self.txtAddress.setEnabled(True)
        self.txtPhone.setEnabled(True)

        self.btnEdit.setVisible(False)
        self.btnDelete.setVisible(False)
        self.btnSave.setVisible(True)

    def save(self):  # SAVE SUPPLIER INFO TO DB
        # Check if 'SUPPLIERS' table exists
        command_2.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SUPPLIERS'")
        if command_2.fetchone()[0] != 'SUPPLIERS':
            query = ('''
                            CREATE TABLE SUPPLIERS 
                            (SupplierID integer PRIMARY KEY, 
                            Name tinytext, 
                            Address varchar(40), 
                            Telephone tinytext)
                    ''')
            command_2.execute(query)
            conn_2.commit()

        Name = self.txtName.text()
        Address = self.txtAddress.text()
        Phone_Num = self.txtPhone.text()

        # Validation for Name, Phone_Num Fields + Updates table
        global NUM_PRESENT_M
        global CHAR_PRESENT_M
        NUM_PRESENT_M = any(map(str.isdigit, Name))
        CHAR_PRESENT_M = any(map(str.isalpha, Phone_Num))

        if not [x for x in (Name, Address, Phone_Num) if x == ""]:  # If not empty
            if NUM_PRESENT_M:  # If num present in 'Name' field
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText("Enter only LETTERS in NAME field")
                msg.exec()
            else:
                if CHAR_PRESENT_M:  # If letter present in 'Phone_Num' field
                    msg = QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText("Enter only NUMBERS in PRICE field")
                    msg.exec()
                else:
                    command_2.execute(f"SELECT Telephone FROM SUPPLIERS WHERE Name = '{Name}'")  # Test Case
                    result = command_2.fetchone()
                    if result is not None:  # If record (Test Case) exists then update
                        command_2.execute(f"SELECT SupplierID FROM SUPPLIERS WHERE Name='{Name}'")
                        Supplier_ID = str(command_2.fetchone()).strip("(,)")

                        query = '''
                                    UPDATE SUPPLIERS SET Name=?, Address=?, Telephone=? WHERE SupplierID=?
                                '''
                        command_2.execute(query, (Name, Address, Phone_Num, Supplier_ID))
                        conn_2.commit()

                        self.txtName.clear()
                        self.txtAddress.clear()
                        self.txtPhone.clear()

                        msg = QMessageBox()
                        msg.setWindowTitle("SUCCESS")
                        msg.setText("Record SUCCESSFULLY updated.")
                        msg.exec()
                    else:  # Else record doesn't exist
                        query = ('''
                                    INSERT INTO SUPPLIERS (Name, Address, Telephone) VALUES (?, ?, ?)
                                ''')
                        command_2.execute(query, (Name, Address, Phone_Num))
                        conn_2.commit()

                        self.txtName.clear()
                        self.txtAddress.clear()
                        self.txtPhone.clear()

                        msg = QMessageBox()
                        msg.setWindowTitle("SUCCESS")
                        msg.setText("Supplier ADDED successfully to contacts")
                        msg.exec()

        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText("Enter ALL values")
            msg.exec()

    def delete(self):  # DELETE SUPPLIER CONTACT FROM DB
        Name = self.txtName.text()
        command_2.execute(f"DELETE FROM SUPPLIERS WHERE Name='{Name}'")
        conn_2.commit()
        msg = QMessageBox()
        msg.setWindowTitle("SUCCESS")
        msg.setText("Supplier REMOVED from contacts.")
        msg.exec()

        self.txtName.clear()
        self.txtAddress.clear()
        self.txtPhone.clear()

        self.btnEdit.setVisible(False)
        self.btnDelete.setVisible(False)
        self.btnSave.setVisible(True)

    def back(self):  # GOES BACK TO HOME WINDOW
        home = Home()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()


class StockReplenishmentWin(QMainWindow, Ui_frmStockReplenishment):
    def __init__(self):  # CONSTRUCTOR METHOD
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(980, 500)
        self.lblUsername.setText(USERNAME)
        self.btnBack.clicked.connect(self.back)
        self.btnReorder.clicked.connect(self.reorder)

        # SHOW LOW LEVEL STOCK ITEMS IN LIST BOX
        ingred_ids = []
        Quantity = []
        MinOrderLvl = []
        self.reorder_names = []
        command_2.execute("SELECT Name, Quantity, MinOrderLvl FROM INGREDIENTS")
        results = command_2.fetchall()
        # Get names for ingreds that are lower than the min req amount needed for restaurant
        for x in results:
            ingred_ids.append(str(x[0]))

            quantity_filter = filter(str.isdigit, x[1])
            quantity = int("".join(quantity_filter).strip())
            Quantity.append(quantity)

            minorderlvl_filter = filter(str.isdigit, x[2])
            minorderlvl = int("".join(minorderlvl_filter).strip())
            MinOrderLvl.append(minorderlvl)
        # If amount in stock < req amount then add those names to array
        for i, q, m in zip(ingred_ids, Quantity, MinOrderLvl):
            if m > q:
                self.reorder_names.append(i)
        # Print those names in the list box
        for name in self.reorder_names:
            self.lstStock.addItem(name)

    def back(self):  # GOES BACK TO HOME WINDOW
        home = Home()
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        self.close()

    def reorder(self):  # REORDER COMPLETED
        string = ""
        for name in self.reorder_names:
            string += name + ", "
        msg = QMessageBox()
        msg.setWindowTitle("SUCCESS")
        msg.setText(f"Re-ordered 100 units more than required amount for {string[:-2]}")
        msg.exec()


'''
3 ingredients below stock levels:
 INGRED ID     |   MEAL NAME
INGRED ID (4)  | Cheese Balls, Grilled Halloumi
INGRED ID (8)  | Cheese Balls, Falafel
INGRED ID (11) | Chocolate Cake, Vanilla CheeseCake, Waffle
'''

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
w = SplashScreen()
w.show()
app.exec()
