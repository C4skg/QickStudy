$(function(){
    'use strict';
    /**
     * this file is for userinfo.html page 
     * and if the user is yourself, it worked
     */
    //upload click
    const input = $('.photo .image')[0];
    $('.uInfo .photo').click(function(){
        let status = $(this).attr('data-status')
        if(status == 'normal'){
            input.click();
        }
    })
    input.addEventListener('change', function(){ 
        $('.uInfo .photo').attr('data-status','waiting')
        var formData = new FormData($('#upload')[0]);
        $.ajax({
            url: window.uploadURI,
            type: "post",
            processData: false,
            contentType: false,
            data: formData,
            success:(e)=>{
                if(e['status']=='success'){
                    swal("成功！","用户头像已更新", "success").then(()=>{
                        let img = $('.uInfo .photo picture img')[0];
                        img.src = `${img.src.split('?')[0]}?time=${new Date().getTime()}`;
                    })
                }else{
                    swal("失败",e['message'], "error").then(()=>{
                        input.value=''
                    })
                }
            },
            error:(e)=>{
                swal("失败",e['message'], "error").then(()=>{
                    input.value=''
                })
                $('.uInfo .photo').attr('data-status','normal')
            },
            complete:(e)=>{
                $('.uInfo .photo').attr('data-status','normal')
            }
        })
    })
})