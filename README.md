# CITS3403-Project-1
What is TGR?
The Game Room, TGR, is an online chat and game room where friends can come together to chat about anything and then decide to team up or verse each other in text-based games to win points and climb the global leader board.
Visiting the Website:
When a user first visits the website they go to the intro page which describes the website and has a button that takes them to the log in page. This page also has a button that goes to the sign-up page if they don’t have an account. Using the nav bar the user can also visit the About us, Privacy Policy and Contact us page. Some of the functionality of these pages, such as the contact us section, is not functional as the website is only locally hosted.
Making an Account:
Using the sign-up page when a user creates an account they must choose a unique username and can add their own profile picture. 
The Home page:
Once on the home page the user can then see their details and empty favourites list on the left. The leader board with the top 3 users in the top middle, the public chat rooms and the join/create private room section in the bottom middle and all the members on the right. The account page can be used to update their details and profile picture.
Joining the public rooms:
They can then join the public chat rooms such as Global, to talk about whatever, Looking for Group, to find people to play with, or Support to ask for help if their confused. The Active Members list shows who is currently in the chat room while the search box in the top right can be used to search all posted messages in the current chat room. By typing "./from" first you can search via username. They can also toggle the active members list and dark mode.
Custom Rooms:
Once they've found some people they can create or join a custom game room and share the join code in the public rooms or via private messages. They can then see the game commands and by running them start a game. Scramble has 3 categories of words each which start a 3 round game where the first to message the correct word wins the round. Hangman starts a cooperative game of hangman where users can talk about what they think they should guess next then one can type "./{letter} to make a guess. These games cannot be started when there’s only 1 active member and game rooms can’t be joined when a game is underway. 
Favouriting and private messages:
If the user has made some friends, they can hit the star button next to their name in the members list to make them a favourite and bring them across to the favourites list. Whether or not they’re a favourite the user can hit the mail icon to private message that user.
Logging Out:
When the user is ready to go, they can hit logout in the nav bar which will log them out and redirect them back to the log in page. 

To Run:
Once all requirements are installed the program can be run from main.py. In init.py it checks if a database exists and if not, so only on the first run, the database initialises with the Computer user and the 3 default chat rooms. On line 88 some code is commented out that adds 20 premade users to the database. This can be uncommented and used to easily show what the Game Rooms should look with many users.

For Testing:
In terminal run 'pytest tests' to run the user tests, run 'pytest selenium-testing' to run the selenium tests.

For Migrations:
To migrate the database after changing it (such as adding or removing a column) run 'flask db migrate' and then 'flask db upgrade'
You may have to set FLASK_APP first. For windows 'set FLASK_APP=main.py' and for Linux and mac 'export FLASK_APP=main.py'

