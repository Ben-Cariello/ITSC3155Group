//Scripts for the swiping on Homepage
//Variables
var swiper = document.getElementById('swipebar');
var startX = 0;
var endX = 0;

swiper.addEventListener("onmousedown",function(event){
    startX = event.screenX;
}, false)

swiper.addEventListener("onmouseup", function(event){
    endX =event.screenX;
    checkDirection(startX, endX);
}, false)

function checkDirection(startX, endX){
    if (startX > endX) {
        swiper.style.backgroundColor = 'yellow';
    }
    if (endX > startX) {
        swiper.style.backgroundColor = 'blue';
    }
    startX = 0;
    endX = 0;
}