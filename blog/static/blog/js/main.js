window.onload=function(){
  startTime();
}
//clock js
function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('txt').innerHTML =
    h + ":" + m + ":" + s;
    var t = setTimeout(startTime, 500);
  }
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}



const mobileNavBar=document.querySelector(".mobile-nav");
const mobileNavLinks=document.querySelectorAll(".mobile-link");
const mobileNavOpenButton=document.querySelector(".nav-open-btn");
const mobileNavCloseButton=document.querySelector(".nav-close-btn");


mobileNavOpenButton.addEventListener('click',displayMobileNavigationBar);


function displayMobileNavigationBar(){

    mobileNavOpenButton.style.display="none";
    mobileNavBar.style.height="80vh";
    mobileNavCloseButton.style.display="block";

    for(i of mobileNavLinks){
        i.style.display="block";
    }
}

mobileNavCloseButton.addEventListener("click",closeMobileNavigationBar);


function closeMobileNavigationBar(){
    mobileNavOpenButton.style.display="block";
    mobileNavBar.style.height="0vh";
    mobileNavCloseButton.style.display="none";

    for(i of mobileNavLinks){
        i.style.display="none";
    }
}
