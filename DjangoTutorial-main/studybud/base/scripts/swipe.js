//Scripts for the swiping on Homepage
//Variables
let startX = 0;
let endX = 0;
const leftButton = document.querySelector('#leftButton');
const rightButton = document.querySelector('#rightButton');;
var bar = document.getElementById('swipeBar');


//Check which way they are swiping
/*function checkDirection(){
    if (startX < endX) {
      rightButton.click();  
    }
    if  (endX < startX) {
        leftButton.click();
    }
}
//Gets start of swipe 
bar.addEventListener("touchstart", (e) => {
    startX = e.changedTouches[0].screenX;
});
//Gets end of swipe and calls checkdriection function
bar.addEventListener("touchend", (e) =>{
    endX = e.changedTouches[0].screenX;
    checkDirection();
});*/

//button clicks
leftButton.addEventListener("click", function(){
    bar.style.backgroundColor = 'yellow';
})

rightButton.addEventListener("click", function(){
    bar.style.backgroundColor = 'red';
})