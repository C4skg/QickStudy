// outline render
$(function(){

    window.addEventListener('scroll',(e)=>{
        let pos = ScrollPos();
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
var ScrollPos = function(){
    // 浏览器适配
    return {
        left: window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft || 0,
        top: window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0
    };
}