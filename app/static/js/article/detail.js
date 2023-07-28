// outline render
$(function(){
    window.addEventListener('scroll',(e)=>{
        let pos = window.ScrollPos();
        if(pos.top >= 100){
            $('.rightContainer').css({
                'left': 0,
                'top': pos.top - 100
            })
        }else{
            $('.rightContainer').css({
                'left': 0,
                'top': 0
            })
        }
    })
})