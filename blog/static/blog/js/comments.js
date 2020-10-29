//Comment form on post details

$('document').ready(
    function(){

        $("#comment-btn").on('click',function(){
            $(".comment-section").slideDown();
        
        })

        $("#cancel-btn").on('click',function(){
            $(".comment-section").slideUp();
        })
    }
)