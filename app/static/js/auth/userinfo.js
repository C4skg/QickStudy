$(function(){
    'use strict';
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
                        window.location.reload();
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
            },
            complete:(e)=>{
                $('.uInfo .photo').attr('data-status','normal')
            }
        })
    })
})