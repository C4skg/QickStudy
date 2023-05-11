$(function(){
    $(".center").delegate("img","click",function(e){
        let element = $(e.currentTarget).clone();
        let m = $("#myModal"),
            content = $(m.find('.modal-content')[0]);
        content.html("");
        content.append(element);
        m.modal('show')
    })
})