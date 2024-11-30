//Scripts for the swiping on Homepage
//Variables
//Declaring Buttons
const denyBut = document.querySelector('#leftButton');
const acceptBut = document.querySelector('#rightButton');
const testPara = document.querySelector('#test');


//Initializing Buttons
denyBut.onclick = denyApp;
acceptBut.onclick = acceptApp;


//Deny application
function denyApp(){
    document.body.style.backgroundColor = "red";
    fetch('/views/get_data/')
    .then(response => response.json())
    .then(data => {
        data.forEach(item => {
            const name = item.name;
            const field = item.field;
            const description = item.description;
            
        });
    });   
}

//accept application
function acceptApp(){
    document.body.style.backgroundColor = "green";
}