const open_btn=document.querySelector('#open-btn');
const close_btn=document.querySelector('#close-btn');
const sidebar=document.querySelector('.side-bar');
const links=document.querySelectorAll('.side-bar-link');
const left_container=document.querySelector('.left');
const link=document.querySelectorAll('.link');
const comment_section=document.querySelector('.comment-section');


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

// sidebar js
open_btn.addEventListener('click',function(){
    left_container.style.width="0%";
    left_container.style.display="none";
    // sidebar.style.display="block";
    sidebar.style.width="100%";
    open_btn.style.display="none";
    close_btn.style.display="inline";

    for(let i of link){
        i.style.display="block";
    }

});

close_btn.addEventListener('click',function(){
    sidebar.style.width="20%";
    open_btn.style.display="inline";
    close_btn.style.display="none";
    left_container.style.width="80%";
    left_container.style.display="block"

    for(let i of link){
        i.style.display="none";
    }
});

// like_button.addEventListener('click',function(){
//     comment_section.style.display="block";
// });

// cancel_button.addEventListener('click',function(){
//     comment_section.style.display="none";
// })

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#blah').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}


