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

var getAllChildren = function(ele,child){
    var children = [];
    ele = $(ele);
    for(let c of ele.find(child)){
        children.push(c);
    }
    for(let c of ele.children(child)){
        children.push(c);
    }
    return children;
}

var emitHighlight = function(ele){ //ele: jQuery object
    let children = getAllChildren(ele,"pre code")
    children.forEach(element => {
        hljs.highlightElement(element);
        hljs.lineNumbersBlock(element);
    })
    
}

$(function(){
    // *md2html
    var center = document.getElementsByClassName("center");
    for(let i=0;i<center.length;i++){
        let ele = center[i],
            code = ele.innerHTML.decode()
        ele.innerHTML = '';
        $(ele).append('<div style="text-align:center;padding: 50px 0;"><span class="spinner-border spinner-border-sm"></span></div>');
        Vditor.md2html(
            code,
            {
                cdn: '/static/Vditor3.9.0'
            }
        ).then(function(e){
            let t = mathJaxTrans(e);
            emitHighlight(t);
            ele.innerHTML = "";
            $(ele).append(t)
        });
    }
})