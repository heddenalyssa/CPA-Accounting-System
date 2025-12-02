Project:
This is a client/tax return system with an OOP design for a small accounting firm.

Database Design:
Schema for tables:

cpa
cpa_name TEXT PRIMARY KEY – the name of the CPA
cpa_assistant TEXT – the name of the CPA’s assistant


clients
client_name TEXT PRIMARY KEY – the name of the client
client_address TEXT – the address of the client
client_income INTEGER – the income of the client
required_materials BOOLEAN DEFAULT FALSE – whether the client has submitted required tax materials
tax_return_id INTEGER REFERENCES tax_returns(tax_return_id) ON DELETE CASCADE – the client’s tax return id
cpa TEXT REFERENCES cpa(cpa_name) – the CPA assigned to the client

tax_returns
tax_return_id SERIAL PRIMARY KEY – the ID of the tax return
filed BOOLEAN DEFAULT FALSE – whether the tax return has been filed
checked BOOLEAN DEFAULT FALSE – whether a CPA has checked the tax return
filed_date DATE – the date the tax return was filed



I chose this design the way I did because it separates the CPA, client, and tax return information, using only the necessary foreign key relationships as overlapping information. Each table focuses on a specific area of the database, which enhances modularity and clarity. The CPA table tracks accountant details and their assistants. The client's table stores name, address, income, and whether required materials have been submitted, while linking each client to their CPA and their unique tax return. The tax_returns table records whether a return has been filed, when it was filed, and whether it has been checked by a CPA. This design allows for easy data management and understanding, and can be expanded in the future if needed.

Software Design: 

The way I chose to design the software promotes modularity and makes the main file easy to read and understand. My overall architecture of the program is having a main menu that the user navigates, and depending on what the user chooses in the menu, the program calls functions to complete those tasks.
