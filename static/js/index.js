window.onload = function(){
    'use strict';
    $(".change").click(function(){
        var dark = $('html').attr('data-user-color-scheme');
        console.log(dark)
        if(dark === undefined){
            $('html').attr("data-user-color-scheme","dark")
        }else{
            $('html').removeAttr('data-user-color-scheme')
        }
    })
}