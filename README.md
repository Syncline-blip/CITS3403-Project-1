# CITS3403-Project-1
What is TGR?
The Game Room, TGR, is an online chat and game room where freinds can come together to chat about anything and then decide to team up or verse each other in text based games to win points and climb the glocal leaderboard. 



To Run:
Once all requirements are installed the program can be run from main.py. In init.py it checks if a database exists and if not, so only on the first run, the database initlilses with the Computer user and the 3 default chat rooms. On line 88 some code is commented out that adds 20 premade users to the database. This can be uncommented and used to easyliy show what the Game Rooms should look with many users.

For Testing:
In terminal run 'pytest tests' to run the user tests, run 'pytest selenium-testing' to run the selenium tests

For Migrations:
To migrate the db after changing it (such as adding or removing a column) run 'flask db migrate' and then 'flask db upgrade'
You may have to set FLASK_APP first. For windows 'set FLASK_APP=main.py' and for Linux and mac 'export FLASK_APP=main.py'