'use strict';
//^ loaded after document


var mathJaxTrans = function(parent){
    var mathObj = $(parent);
    for(let element of mathObj){
        if ($(element).attr('class') == 'language-math'){
            let render = element.innerHTML.decode();
            katex.render(render,element)
        }
    }
    for(let element of mathObj.find('.language-math')){
        let render = element.innerHTML.decode();
        katex.render(render,element)
    }
    return mathObj;
}

var emit = function(){
    hljs.highlightAll();
    hljs.initLineNumbersOnLoad ({ singleLine:true });
}

$(function(){
    // *md2html
    var center = document.getElementsByClassName("center");
    for(let i=0;i<center.length;i++){
        let ele = center[i]
        Vditor.md2html(
            ele.innerHTML.decode(),
            {
                cdn: '/static/Vditor3.9.0'
            }
        ).then(function(e){
            let t = mathJaxTrans(e);
            ele.innerHTML = '';
            $(ele).append(t)
            if(i == center.length -1 ){
                emit();
            }
        });
    }
    
})