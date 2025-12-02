import database
from models.Client import Client
from models.Cpa import Cpa
from connection_pool import init_pool, get_connection

# This file provides the command-line interface for the client/tax return system handling
# user input, displaying the menu, and calls functions that interact with
# the database and object-oriented models.


DATABASE_PROMPT = "Enter the DATABASE_URL value or leave empty to load from .env file: "
MENU_PROMPT = """-- Menu --

1) Add a Client
2) Add a CPA
3) Check/Submit Required Materials
4) Check/Mark Tax Return if filed
5) Check/Mark if CPA checked a return
6) Exit

Enter your choice: """

# functions

#adding functions
def add_client(): #Adds a clients to the database, checks if they have a CPA
    client_name = input("Enter client's name: ")
    client_address = input("Enter client's address: ")
    client_income = int(input("Enter client's income: "))
    required_materials = input("Does the client have the required materials?(Yes/no): ").strip().lower() == 'yes'
    cpa_name = input("Enter client's CPA: ")

    with get_connection() as connection:
        if not database.cpa_exists(connection, cpa_name):
            print("CPA does not exist in database. Please create CPA profile.\n")
            add_cpa_if_not_exist(cpa_name)

    with get_connection() as connection:
        tax_return_id = database.create_blank_tax_return(connection)

    client = Client(client_name, client_address, client_income, required_materials, tax_return_id, cpa_name)
    client.save()


def add_cpa(): #Adds a CPA and the assistant to the database
    cpa_name = input("Enter CPA: ")
    cpa_assistant = input("Enter CPA Assistant: ")
    cpa = Cpa(cpa_name, cpa_assistant)
    cpa.save()


def add_cpa_if_not_exist(cpa_name): #Adds a cpa from the choice on the menu
    cpa_assistant = input("Enter CPA Assistant: ")
    cpa= Cpa(cpa_name, cpa_assistant)
    cpa.save()

#checking functions

def check_required_materials(): #Checks if a client has submitted their required materials
    client_name = input("Enter client's name you would like to check the required materials for: ")
    with get_connection() as connection:
        try:
            client = Client.get(connection, client_name)  # Load the client object
        except ValueError as e:
            print(e)
            return
    if client.required_materials:
        print("Required materials are submitted.")
    else:
        user_input = input("Required materials are not submitted. Would you like to submit them now?(Yes/No): ").strip().lower()
        if user_input == "yes":
            client.submit_materials()
            print("Materials successfully submitted.")


def status_tax_return_filed(): #Checks if a clients tax return has been filed, then gives the option to file it
    client_name = input("Enter client's name you would like to check the tax return status for: ")
    with get_connection() as connection:
        try:
            client = Client.get(connection, client_name)
        except ValueError as e:
            print(e)
            return
    status = client.get_tax_return_status()
    if status["filed"] and status["checked"]:
        print(f"Tax return was filed on {status["filed_date"]}.\nTax return has been checked by a CPA.")

    elif status["filed"] and not status["checked"]:
        print(f"Tax return was filed on {status["filed_date"]}.\nTax return has not been checked by a CPA.\n")
        checking_input = input("Would you like to do that now(Yes/no)?: ").strip().lower()
        if checking_input == "yes":
            client.check_tax_return()
        else:
            return
    else:
        user_input = input("Tax return is not filed. Would you like to do that now?(Yes/No): ").strip().lower()
        if user_input == "yes":
            cpa_input = int(input("Are you a 1. Cpa or an 2. Assistant?: "))
            if cpa_input == 1:
                client.file_tax_return()
                client.check_tax_return()
                print("Tax Return successfully filed and checked.")
            elif cpa_input == 2:
                client.file_tax_return()
                print("Tax Return successfully filed.")
            else:
                print("Invalid input.")


def check_tax_return_cpa(): #Checks if a clients ta return has been checked by a CPA, then gives the option to do so.
    client_name = input("Enter client's name you would like to check the tax return status for: ")
    with get_connection() as connection:
        try:
            client = Client.get(connection, client_name)
        except ValueError as e:
            print(e)
            return
    status = client.get_tax_return_status()
    if status["checked"]:
        print("Tax return was checked by a Cpa.")
    else:
        user_input = input("Tax return has not been checked by a Cpa. Would you like to do that now(Yes/no)?: ").strip().lower()
        if user_input == "yes":
            client.check_tax_return()


#Main Menu Options
MENU_OPTIONS = {
    "1": add_client,
    "2": add_cpa,
    "3": check_required_materials,
    "4": status_tax_return_filed,
    "5": check_tax_return_cpa
}



def menu(): #initilizing the database connection pool, creates tables, and runs the main menu loop
    db_url = input(DATABASE_PROMPT).strip()
    if db_url:
        init_pool(db_url)  #initializing pool with user-provided URL
    else:
        init_pool()  #initializing pool from my .env

    with get_connection() as connection:
        database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "6":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")


if __name__ == "__main__":
    menu()
