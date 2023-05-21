  // Event listener for settings
  document.addEventListener('DOMContentLoaded', (event) => {
    const toggleMembersButton = document.querySelector('#toggle-members-btn');
    const darkModeToggleBtn = document.querySelector('#dark-mode-toggle-btn');
    const membersList = document.querySelector('.members-list');
    const body = document.body;
    const messages = document.getElementById('messages');

    const mq = window.matchMedia("(max-width: 767px)");

    toggleMembersButton.addEventListener('click', () => {
      let isMobile = mq.matches; // Check the viewport size at the moment of click
      if (isMobile) {
        membersList.classList.toggle('hidden-mobile');
        if (!membersList.classList.contains('hidden-mobile')) {
          membersList.style.display = 'block';
        }
      } else {
        membersList.classList.toggle('hidden');
        if (membersList.classList.contains('hidden')) {
          membersList.style.display = 'none';
        } else {
          membersList.style.display = 'block';
        }
      }
    });

    darkModeToggleBtn.addEventListener('click', () => {
      body.classList.toggle('dark-mode');
      messages.classList.toggle('dark-mode');
    });
});


  //This is used to add a Member to Active Members list in a chat room.
  const addMember = (username, profile_picture) => {
    const content = `
      <div>
        <span class="one-user" id="${username}">
          <img src="${profile_picture}" alt="Profile Picture" width="50" height="50" style="border-radius: 50%;"> <strong>${username}</strong>
        </span>
      </div>
    `;
    members_list.innerHTML += content;
  }

  //This is mainly used to remove someone fom the Active Members list, in which case the 'itemID' is their username which
  // is used for the id of their span when adding them to the Active Members list initially.
  function removeItem( itemID ){
    let element = document.getElementById(itemID);
    element.parentNode.removeChild(element);
  }

  general_rooms = ["GLOB", "LFGG", "SUPP"] //These are the hard coded public chat rooms that never change.
  socketio.on("message", (data) =>{
        title = document.getElementById("title").innerHTML
        index = title.indexOf(": ");
        roomName = title.slice(index+2,index+6);
        //If a room has game support then we show the available commands. 
        if(!(general_rooms.includes(roomName))){
          document.getElementById("commandsDiv").style.visibility = "visible";
        }

        if(!(typeof data.all_member_usernames === "undefined"))
        {
            //This has to be a new connection to the room. (only message parsed without a date)
            addMember(data.username, data.profile_picture);
            for(i=0; i < data.all_member_usernames.length; i++){
              let myEle = document.getElementById(data.all_member_usernames[i]);
              if(!myEle) { //If they're not in the list add them.
                addMember(data.all_member_usernames[i], data.all_member_profiles[i]);
              }
            }

        }else if(!data.message.includes("has left the room")){
          createMessage(data.username, data.message, data.profile_picture, data.date);
        }
        

        //If scramble game is going, then we fetch the latest word and display it at the top of screen.
        if (data.message.includes("Unscramble this word:") && data.username == "CP"){
          i = data.message.lastIndexOf(': ');
          showCurrentWord(data.message.slice(i+2)); //This grabs the current word from the HTML through JS.
          callTimer(0, 11); 
        
        //If the game is over, stop the timer. 
        }else if(data.message.includes("Game Over!") ){
            stopTimer();
        //If Computer has sent a message saying Hangman has started then start the 1 minute timer.
        }else if (data.message.includes("Hangman Started") && data.username == "CP"){
            callTimer(1,1);
        
        //When the computer sends the latest hangman updated word we showcase it at the top of the screen.
        }else if(data.message.includes("_") && data.username == "CP"){
          document.getElementById("game-answer").innerHTML = `<span id="hangmanWord">Current Word: ${data.message}</span>`;
        

        }else if(data.message.includes("Out of lives!") && data.username == "CP"){
            stopTimer();
        }else if(data.message.includes("Stopped") && data.username == "CP"){
            stopTimer();
        }else if(data.message.includes("CORRECT") && data.username == "CP"){
            stopTimer();
        }
        
        //If a user is leaving the chat room then we need to remove them from the Active Members.
        if(!(typeof data.disconnecting === "undefined"))
        {
          removeItem(data.username);
        }
      });

  const sendMessage = () => {
      const message = document.getElementById("message")
      if (message.value == "") return;
      socketio.emit("new-message", {data: message.value}) //This is an event called new-message, altering the name allows more complicated things.
      message.value = ""; 
  };



/* Does the setup for starting the timer and then calls startTimer() to start it.

  Because of the delay to show to screen the timer input must be 1 seond above desired time, so 10 second 
  countdown requires input argument of 11 seconds.
*/ 
function callTimer(min, seconds){
    document.getElementById('timer').innerHTML = min + ":" + seconds;
    document.getElementById("clock-and-game-answer").style.visibility = "visible";
    document.getElementById("timer").style.visibility = "visible"; 
    document.getElementById("clock-and-game-answer").style.height = "6vh";
    document.getElementById("messages").style.height = "64vh";
    startTimer();
}

function startTimer() {
    var presentTime = document.getElementById('timer').innerHTML;
    var timeArray = presentTime.split(/[:]+/);
    var m = timeArray[0];
    var s = checkSecond((timeArray[1] - 1));
    if(s==59){m=m-1}
        if(m<0){
            //Hides the elements when the timer runs out.
            document.getElementById("clock-and-game-answer").style.visibility = "hidden";
            document.getElementById("timer").style.visibility = "hidden";
            document.getElementById("clock-and-game-answer").style.height = 0;
            document.getElementById("messages").style.height = "70vh";
            socketio.emit("timer-done");
            return
        }
    document.getElementById('timer').innerHTML = m + ":" + s;
    timerTimeout = setTimeout(startTimer, 1000);
    
    }

    function stopTimer() {
        document.getElementById("clock-and-game-answer").style.visibility = "hidden";
        document.getElementById("timer").style.visibility = "hidden";
        document.getElementById("clock-and-game-answer").style.height = 0;
        document.getElementById("messages").style.height = "70vh"
        clearTimeout(timerTimeout);
      }

    //Called when a user joins and the game has already begun.
    function showTimer() {
      document.getElementById("clock-and-game-answer").style.visibility = "visible";
      document.getElementById("timer").style.visibility = "visible";
      var currentTime = document.getElementById("timer").innerHTML;
      document.getElementById("current-time").innerHTML = "Time: " + currentTime;
    }

    function checkSecond(sec) {
    if (sec < 10 && sec >= 0) {sec = "0" + sec}; // add zero in front of numbers < 10
    if (sec < 0) {sec = "59"};
    return sec;
    }


    //These are used if we want to insert a new div, but I might revert to just adding the word under the timer.
    function showCurrentWord(word){
      const currentWord = `<span id="scrambleWord">Current Word: ${word}</span>`
      document.getElementById("game-answer").innerHTML = currentWord;
    }

    var input = document.getElementById("message");
    input.addEventListener("keypress", function(event) {
      if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send-btn").click();
      }
    });


      //Adds the ability to just click enter and not have to press "Send" button for messages
      var input = document.getElementById("message");
      input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
          event.preventDefault();
          document.getElementById("send-btn").click();
        }
      });

      const createMessage = (username, msg, profile_picture, date) => {
        const messageType = (username === myUsername) ? "my-message" : "other-message";
        const content = `
            <div class="${messageType}">
                <img src="${profile_picture}" alt="Profile Picture" width="50" height="50" style="border-radius: 50%;">
                <div class="message-content">
                    <span class="date" style="font-size: 0.8em; display: block;">${date}</span>
                    <span><strong>${username}</strong>: ${msg}</span>
                </div>
            </div>
        `;
        messages.innerHTML += content;
    

        //This scroll means it's a lot smoother and not so jumpy.
        messages.scrollTo({
          top: messages.scrollHeight,
          behavior: 'smooth'
        },);
    
    };


    