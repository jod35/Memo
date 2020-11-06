$("document").ready(
    function(){
        $("#create-post").on("click",function(){
            $(".post-form").slideDown(1200);
        });

        $(".cancel-btn").on("click",function(){
            $(".post-form").slideUp(1200);
        });
    }
)
