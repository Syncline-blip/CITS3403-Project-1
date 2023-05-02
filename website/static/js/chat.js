let allMessages = ['Message1', 'Message2'];

const resultsBox = document.querySelector(".result-box");
const searchBar = document.querySelector("#searchBar");

searchBar.onkeyup = function(){
    let result = [];
    let input = searchBar.value;
    if(input.length){
        result = allMessages.filter((keyword)=>{
           return keyword.toLowerCase().includes(input.toLowerCase());
        });
        console.log(result);
    }
    display(result);

    if(!result.length){
        resultsBox.innerHTML = '';
    }
}

searchBar.focusout = function(){
    resultsBox.innerHTML = '';
}

function display(result){
    const content = result.map((list)=>{
        return "<li>" + list + "</li>";
    });

    resultsBox.innerHTML = "<ul>" + content.join('') + "</ul>"
}