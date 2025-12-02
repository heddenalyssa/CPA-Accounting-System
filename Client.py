import database
from connection_pool import get_connection

# This file defines the Client class in the system.
# It holds client details and provides methods to interact with the database,
# including submitting materials and managing tax return status.



class Client:
    def __init__(self, client_name: str, client_address: str, client_income: int,
                 required_materials: bool = False, tax_return_id: int = None, cpa: str = None):
        self.client_name = client_name
        self.client_address = client_address
        self.client_income = client_income
        self.required_materials = required_materials
        self.tax_return_id = tax_return_id
        self.cpa = cpa

    def __repr__(self):
        return f"Client {self.client_name} | Income: {self.client_income} | CPA: {self.cpa}"

    def save(self):
        with get_connection() as connection:
            database.add_client(connection, self.client_name, self.client_address, self.client_income, self.required_materials, self.tax_return_id, self.cpa)



    def submit_materials(self):
        with get_connection() as connection:
            database.update_required_materials(connection, self.client_name)

    @classmethod
    def get(cls, connection, client_name):  #getting the client
        result = database.get_client(connection, client_name)
        if result:
            return cls(*result)
        else:
            raise ValueError(f"Client '{client_name}' not found in database.")

    def get_tax_return_status(self): #checking the tax return
        with get_connection() as connection:
            result = database.get_tax_return(connection, self.tax_return_id)
            if result:
                client_id, filed, checked, filed_date = result
                return {
                    "client_id": client_id,
                    "filed": filed,
                    "checked": checked,
                    "filed_date": filed_date
                }
            else:
                return None

    def check_tax_return(self):  #checking the tax return
        with get_connection() as connection:
            database.check_tax_return(connection, self.tax_return_id)

    def file_tax_return(self):  #filing the tax return
        with get_connection() as connection:
            database.file_tax_return(connection, self.tax_return_id)
