'use strict';
//^ loaded after document


var mathJaxTrans = function(parent){
    var mathObj = $(parent);
    var _trans = function(element){
        let render = element.innerHTML.decode();
        katex.render(render,element)
        element.setAttribute('data-syntax',render)
        element.setAttribute('data-copy','Copy')
    }
    for(let element of mathObj){
        if ($(element).attr('class') == 'language-math'){
            _trans(element)
        }
    }
    for(let element of mathObj.find('.language-math')){
        _trans(element)
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
        hljs.addCopyButton(element);  
    })
}

$(function(){
    // *md2html
    var center = document.getElementsByClassName("center"),
        mathList = [];
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
            mathList.push(t);
        });
    }
    // *数学公式可复制
    $(".center").on("click", ".language-math", function(e) {
        if($(e.currentTarget).attr('data-copy') == 'Copy'){
            let _syntax = $(e.currentTarget).attr('data-syntax');
            var el = document.getElementById('katex-copy-el');
            if (!el) {
                el = document.createElement("textarea");
                el.style.position = "absolute";
                el.style.left = "-9999px";
                el.style.top = "0";
                el.id = 'katex-copy-el';
                document.body.appendChild(el);
            }
            el.textContent = _syntax;
            el.select();
    
            try {
                var successful = document.execCommand('copy');
                if (successful) {
                    $(e.currentTarget).attr('data-copy','Success');
                    setTimeout(function () {
                        $(e.currentTarget).attr('data-copy','Copy');
                    }, 2000);
                }else{
                    $(e.currentTarget).attr('data-copy','Success');
                }
            } catch (err) {
                target.dataset.title = TEXT_ERROR;
            }
        }
    });
})