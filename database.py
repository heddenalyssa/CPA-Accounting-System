from contextlib import contextmanager

# This file is all the SQL queries and database functions for the client/tax return system.
# It's responsible for creating tables, inserting and retrieving data, and updating statuses.


# --- create table queries --

CREATE_CPA = """CREATE TABLE IF NOT EXISTS cpa (
    cpa_name TEXT PRIMARY KEY,
    cpa_assistant TEXT
);"""

CREATE_CLIENTS = """CREATE TABLE IF NOT EXISTS clients (
    client_name TEXT PRIMARY KEY,
    client_address TEXT,
    client_income INTEGER,
    required_materials BOOLEAN DEFAULT FALSE,
    tax_return_id INTEGER REFERENCES tax_returns(tax_return_id) ON DELETE CASCADE,
    cpa TEXT REFERENCES cpa(cpa_name)
);"""

CREATE_TAX_RETURN = """CREATE TABLE IF NOT EXISTS tax_returns (
    tax_return_id SERIAL PRIMARY KEY,
    filed BOOLEAN DEFAULT FALSE,
    checked BOOLEAN DEFAULT FALSE,
    filed_date DATE
);"""

# selection
SELECT_CLIENT = "SELECT * FROM clients WHERE client_name = %s;"
SELECT_TAX_RETURN = "SELECT * FROM tax_returns WHERE tax_return_id = %s;"

#insertion
INSERT_CLIENT = "INSERT INTO clients (client_name, client_address, client_income, required_materials, tax_return_id, cpa) VALUES (%s, %s, %s, %s, %s, %s);"
INSERT_CPA = "INSERT INTO cpa (cpa_name, cpa_assistant) VALUES (%s, %s);"
INSERT_TAX_RETURN ="INSERT INTO tax_returns DEFAULT VALUES RETURNING tax_return_id;"

#checking
CHECK_IF_CPA_EXISTS = "SELECT * FROM cpa WHERE cpa_name = %s;"

#updating
UPDATE_REQUIRED_MATERIALS = "UPDATE clients SET required_materials = TRUE WHERE client_name = %s;"
UPDATE_FILED_STATUS= "UPDATE tax_returns SET filed_date = CURRENT_DATE, filed = TRUE WHERE tax_return_id = %s;"
UPDATE_CHECK_STATUS = "UPDATE tax_returns SET checked = TRUE WHERE tax_return_id = %s;"


@contextmanager
def get_cursor(connection):  # this is context manager for a context manager
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables(connection): #creating the tables
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_TAX_RETURN)
        cursor.execute(CREATE_CPA)
        cursor.execute(CREATE_CLIENTS)


# -- other functions ---
def add_client(connection, client_name, client_address, client_income, required_materials, tax_return_id, cpa): #adding clients
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_CLIENT, (client_name, client_address, client_income, required_materials, tax_return_id, cpa))


def add_cpa(connection, cpa_name, cpa_assistant): #adding cpas
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_CPA, (cpa_name, cpa_assistant))


#get

def get_client(connection, client_name): #retrieving client information
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_CLIENT, (client_name,))
        return cursor.fetchone()

def get_tax_return(connection, tax_return_id): #retrieving tax return information
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_TAX_RETURN, (tax_return_id,))
        return cursor.fetchone()

#update

def update_required_materials(connection, client_name): #updating the required materials
    with get_cursor(connection) as cursor:
        cursor.execute(UPDATE_REQUIRED_MATERIALS, (client_name, ))

def check_tax_return(connection, tax_return_id): #checkin the tax return checked status
    with get_cursor(connection) as cursor:
        cursor.execute(UPDATE_CHECK_STATUS, (tax_return_id,))

def file_tax_return(connection, tax_return_id): #filing the tax return
    with get_cursor(connection) as cursor:
        cursor.execute(UPDATE_FILED_STATUS, (tax_return_id,))



#exsists

def cpa_exists(connection, cpa_name): #checking if a cpa exists
    with get_cursor(connection) as cursor:
        cursor.execute(CHECK_IF_CPA_EXISTS, (cpa_name, ))
        result = cursor.fetchall()

    return len(result) > 0

#other

def create_blank_tax_return(connection): #creating a blank tax return that is tied to a client when a client is created.
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_TAX_RETURN)
        return cursor.fetchone()[0]