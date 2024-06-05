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

(1) When starting the webapp, you should be able to run through a long list of active and inactive players.

(2) You can use the search bar to specify which players you are looking for, e.g:

        'Dan' should list all players containing this sequence of letters. This search bar IS NOT case-sensitive.

(3) The height filter demands a specific type of input. Since the height is denoted according to the imperial system, you should feed the webapp with an input of this sort:

        Max-height = 6-0    ,    Min-height = 6-2

(4) Clicking on a player moves you to a section providing informations about the specific player.

(5) You can use the 'Teams' button on the main page to access a list of all the NBA teams. From here you can click on a specific team to get further information.