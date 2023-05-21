# CITS3403-Project-1
What is TGR?
The Game Room (TGR) is an online chat room where users can come together to chat and play text-based games to win points and climb the global leader board.

Visiting the Website:
When users first visit the website they land on the intro page. This page provides a brief description of the application and has a button that leads to the log in page. From there, users can sign-up if they do not have an account. Using the nav bar, users can also visit the About us, Privacy Policy and Contact us pages. As the website is hosted locally, we did not implement functionality on the forms and buttons on About Us and Contact Us. Information regarding the project team details can be found on the About Us Page. 

Making / Updating an Account:
Users can create an account using the Sign Up page. The form requires users to enter an email address, unique username, password and profile picture.
Users can also update their account information in the Account tab after signing in.

The Home Page:
The home page displays information on the user, the global leaderboard, other users on TGR and the chatrooms. 
The user information displays their profile picture and total cumulative score. 
The leader board features the top 3 highest scoring users with a list below, of lower scores. 
The member list shows all users that have created an account with options to create a private chat and favourite the user.
The public chat rooms features three buttons, Global Chat, Looking For Chat and Support Chat, which all create a chat room. These rooms are just for chatting, to play the games, users have to create a new room or join a room. 

Joining Public Rooms:
The public chat rooms are accessible to all users. 
Global chat is for any/all topics, Looking For Group Chat is for users to connect with others to play games and Support Chat is for users to help each other.

Within Chat Rooms:
The chat rooms feature the room code, a search bar for chat history, a list of active members and the chat box. 
The room code is generated and can be shared with others to join the current chat.
The search bar can be used to search for messages and phrases. This returns the user, and the date/time of messages containing the search parameter. Messages can also be searched by user.
The Active Members list shows all users in the chat room.
On the right of the message text input, there is a settings tool where users can hide the Active Members list and change the appearance of the chat room to dark mode. 

Creating Rooms:
When users would like to play games, they can create or join a custom room. Users will need to share the room code with others to join, as the games are not available in the Public Chat Rooms or private chats. In these rooms, a list of commands are displayed on the left of the chat box which are typed to run the games.
We currently feature two games, Scramble and Hangman.
Scramble is a game that takes a category (fruit, videogames, css) and generates a word where the letters are scrambled. Users have to guess the correct word and whoever guesses it first, wins.
Hangman is a game where users have to guess letters of a word within one minute. Users can submit a guess by typing ./{letter} e.g. ./a to guess the letter a. This way users can chat whilst they play.

Logging Out:
When users are done, they can log out via the navigation bar. After logging out, users will be redirected to the Log In page.

To Run:
Once all requirements are installed the program can be run from main.py. In init.py, this checks if a database exists and if not, on the first run, the database initialises with the Computer user and the 3 default chat rooms. 
On line 88 the commented-out code, adds 20 pre-made users to the database. This can be uncommented to show what the Game Rooms should look with multiple users.

Testing:
In terminal run 'pytest tests' to run the user tests.
To run selenium tests make sure the main app is running then run 'pytest selenium-testing' to run the selenium tests.

Migrations:
To migrate the database after changing it (such as adding or removing a column) run 'flask db migrate' and then 'flask db upgrade'.
You may have to set FLASK_APP first. For windows 'set FLASK_APP=main.py' and for Linux and mac 'export FLASK_APP=main.py'.

