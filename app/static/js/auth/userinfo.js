$(function(){
    'use strict';
    //upload click
    const input = document.getElementById('uImgPhoto');
    $('.uInfo .photo').click(function(){
        input.click();
    })
    input.addEventListener('change', function(){
        let form = document.createElement('form')
        form.appendChild(this);
        $.ajax({
            url: window.uploadURI,
            type: "post",
            data: $(form).serialize(),
            success:(e)=>{
                console.log(e);
            },
            error:(e)=>{
                console.log(e);
            },
            complete:(e)=>{
                console.log(e);
            }
        })
    })
})