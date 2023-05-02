let allMessages = [];

const resultsBox = document.querySelector(".result-box");
const searchBar = document.querySelector("#searchBar");

searchBar.onkeyup = function(){
    let result = [];
    let input = searchBar.value;
    if(input.length){
        let msgs = document.getElementsByClassName("a-message");
        for(i = 0; i < msgs.length; i++){
            if(!allMessages.includes(msgs[i].innerHTML)){ 
                allMessages.push(msgs[i].innerHTML);
            }}
        result = allMessages.filter((keyword)=>{
           return keyword.toLowerCase().includes(input.toLowerCase());
        });
    }
    display(result);

    if(!result.length && input.length){
        resultsBox.innerHTML = "<ul>" + "<strong>No Results</strong>" + "</ul>";
    }
}

searchBar.focusout = function(){
    resultsBox.innerHTML = '';
}

function display(result){
    const content = result.map((list)=>{
        return "<li onclick=scrollFunction()>" + list + "</li>";
    });
    resultsBox.innerHTML = "<ul>" + content.join('') + "</ul>"

}

function scrollFunction(){
    console.log("Click detected");
}