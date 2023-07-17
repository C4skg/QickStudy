'use strict';
//^ loaded after document

var mathJaxTrans = function(parent){
    var div = document.createElement('div');
    div.innerHTML = parent
    var mathObj = div.querySelectorAll('.language-math');
    for(let element of mathObj){
        let render = element.innerHTML.decode();
        katex.render(render,element)
        element.setAttribute('data-syntax',render)
        element.setAttribute('data-copy','Copy')
    }
    return div;
}

var emitHighlight = function(ele){ //ele: document object
    let children = ele.querySelectorAll('pre code');
    console.log(children)
    children.forEach(element => {     
        hljs.highlightElement(element);
        hljs.lineNumbersBlock(element);
        hljs.addCopyButton(element);  
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
                cdn: '/static/Vditor'
            }
        ).then(function(e){
            let t = mathJaxTrans(e);
            emitHighlight(t);
            ele.innerHTML = "";
            $(ele).append(t.innerHTML)
            for(let i=1;i<=6;i++){
                // console.log(t.querySelectorAll(`h${i}`))
            }
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
    
    // *markdown 主题提取
})