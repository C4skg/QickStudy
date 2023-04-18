'use strict';
//^ loaded after document


var mathJaxTrans = function(){
    var mathObj = document.getElementsByClassName('language-math');
    for(let element of mathObj){
        let render = element.innerHTML.decode();
        katex.render(render,element)
    }
}

$(function(){
    // *md2html
    var center = document.getElementsByClassName("center")[0]
    Vditor.md2html(center.innerHTML.decode()).then(function(e){
        center.innerHTML = e
        hljs.highlightAll();
        hljs.initLineNumbersOnLoad ({ singleLine:true });
        mathJaxTrans();
    });
})