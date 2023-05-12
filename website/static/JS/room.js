

// var socketio = io();

// const messages = document.getElementById("messages");
// const members_list = document.getElementById("membersList");


// const addMember = (username, profile_picture) => {
// const content = `
//     <div>
//     <span class="one-user" id="${username}">
//         <img src="${profile_picture}" alt="Profile Picture" width="50" height="50" style="border-radius: 50%;"> <strong>${username}</strong>
//     </span>
//     </div>
// `;
// members_list.innerHTML += content;
// }

// function removeItem( itemID ){
// let element = document.getElementById(itemID);
// element.parentNode.removeChild(element);
// }

// const createMessage = (username, msg, profile_picture, date) => {
// const content = `
//     <div>
//     <span class="a-message">
//         <img src="${profile_picture}" alt="Profile Picture" width="50" height="50" style="border-radius: 50%;">
//         <span><strong>${username}</strong>: ${msg}</span>
//         <span class="date">${date}</span>
//     </span>
//     </div>
// `;
// messages.innerHTML += content;

// //Scroll to bottom after posting message
// messages.scrollTop = messages.scrollHeight;
// };



// socketio.on("message", (data) =>{
//     if(!(typeof data.all_member_usernames === "undefined"))
//     {
//         addMember(data.username, data.profile_picture);
//         for(i=0; i < data.all_member_usernames.length; i++){
//             let myEle = document.getElementById(data.all_member_usernames[i]);
//             if(!myEle) { //If they're not in the list add them.
//             addMember(data.all_member_usernames[i], data.all_member_profiles[i]);
//             }
//         }

//     }
//     createMessage(data.username, data.message, data.profile_picture, data.date);
//     // if (data.message.includes("Unscramble this word:") && data.username == "CP"){
//     //      callTimer();
//     // }else if (data.message.includes("is CORRECT") && data.username == "CP"){
//     //     stopTimer();
//     //     console.log("IN HERE ")
//     // }
    
//     if(!(typeof data.disconnecting === "undefined"))
//     {
//         removeItem(data.username);
//     }

//     });

// const sendMessage = () => {
//     const message = document.getElementById("message")
//     if (message.value == "") return;
//     socketio.emit("new-message", {data: message.value}) //This is an event called new-message, altering the name allows more complicated things.
//     message.value = ""; 
// }

// function callTimer(){
//     document.getElementById('timer').innerHTML = 0 + ":" + 31;
//     document.getElementById("clock").style.visibility = "visible"; 
//     document.getElementById("clock").style.height = "10%";
//     startTimer();
// }

// function startTimer() {
//     var presentTime = document.getElementById('timer').innerHTML;
//     var timeArray = presentTime.split(/[:]+/);
//     var m = timeArray[0];
//     var s = checkSecond((timeArray[1] - 1));
//     if(s==59){m=m-1}
//         if(m<0){
//             //Hides the elements when the timer runs out.
//             document.getElementById("clock").style.visibility = "hidden";
//             document.getElementById("clock").style.height = 0;
//             return
//         }
    
//     document.getElementById('timer').innerHTML = m + ":" + s;
//     timerTimeout = setTimeout(startTimer, 1000);
    
//     }

//     function stopTimer() {
//         document.getElementById("clock").style.visibility = "hidden";
//         document.getElementById("clock").style.height = 0;
//         clearTimeout(timerTimeout);
//       }

//     function checkSecond(sec) {
//     if (sec < 10 && sec >= 0) {sec = "0" + sec}; // add zero in front of numbers < 10
//     if (sec < 0) {sec = "59"};
//     return sec;
//     }

//     // Adds the ability to just click enter and not have to press "Send" button for messages
//     var input = document.getElementById("message");
//     input.addEventListener("keypress", function(event) {
//       if (event.key === "Enter") {
//         event.preventDefault();
//         document.getElementById("send-btn").click();
//       }
//     });

    
    