# NBA Search Engine

# running the webapp:

Assuming that the system contains a modern and functional Python 3 & SQL installation, these are the steps to run the webapp:

(1) Run the following code to make sure your system is familiar with all the necessary modules:
>$ pip install -r requirements.txt

(2) Initialize the database by executing the three SQL files to create the necessary tables. This can as an example be done through the pgAdmin 4 query tool (Assuming that this is available to the user) or by typing in the following postgreSQL command into the terminal:
>$ psql -U <user_name> -d <database_name> -f path/to/the/file.SQL

# Example

        psql -U JohnDoe -d NBA_DB -f Users/JohnDoe/Desktop/KU/DIS/NBA-database-app/SRC/sql/CreatePlayers.SQL

(3) In the app.py-file, insert your own database username and password

(4) Run the webapp through:
>$ python3 SRC/app.py

_________________________________________________________________________

# Navigating in the webapp