import database
from connection_pool import get_connection

# This file defines the Cpa class in the system.
# It stores CPA details and provides methods to save them into the database.


class Cpa:
    def __init__(self, cpa_name: str, cpa_assistant: str):
        self.cpa_name = cpa_name
        self.cpa_assistant = cpa_assistant

    def __repr__(self):
        return f"Cpa {self.cpa_name} | Assistant: {self.cpa_assistant} "

    def save(self):
        with get_connection() as connection:
            database.add_cpa(connection, self.cpa_name, self.cpa_assistant)