$(function(){
    'use strict';
    // while runtime
    (function(doc,win){
        changeMode();
        checkDev();
        //drop-menu
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl)
        })
    })(document,window);

    $(".modeButton").click(function(){
        var mode = isDark() ? '' : 'dark';
        changeMode(mode);
    })
    $(".scrollTop").click(function(){
        $('body,html').animate({
            scrollTop:0
        },1);
    })
    function changeMode(mode=null){
        if(mode == null){
            mode = isDark() ? 'dark' : '';
        }else{
            localStorage.setItem('dark',mode == 'dark');  
        }
        var node = $("*");
        if(mode == 'dark'){
            $('html').attr('data-bs-theme','dark')
        }else{
            $('html').removeAttr('data-bs-theme')
        }
        // 按钮
        var btn = $('.modeButton');
        if(btn.length >= 1){
            for(let eve of btn){
                var children = $(eve).children('i');
                for(let child of children){
                    let jQChild = $(child);
                    let attr = jQChild.attr('class').split(' ');
                    if(attr.includes('fa')){
                        attr.remove('fa-sun-o','fa-moon-o');
                        if(mode == 'dark'){
                            attr.push('fa-sun-o');
                        }else{
                            attr.push('fa-moon-o');
                        }
                        jQChild.attr('class',attr.join(' '))
                        break; 
                    }
                }
            }
        }
        //!codeBlock
        var codeBlock = $('#hljsCodeBlockColor');
        if(typeof codeBlock === 'object'){
            let href = codeBlock.attr('href');
            if(href && typeof href === 'string'){
                if(mode == 'dark'){
                    href = href.replace('emacs.css','native.css')
                }else{
                    href = href.replace('native.css','emacs.css')
                }
                codeBlock.attr('href',href);
            }
        }
    }

    function isDark(){
        var dark = localStorage.getItem('dark') == 'true';
        var html = $('html').attr('data-bs-theme') == 'dark';
        return !!(dark || html);
    }

    function checkDev(){
        let top = ScrollPos().top,
            hidened = true;
        let dev = $('.rightbottom');
        if(dev.length == 0) return;
        if(top >= 600 && hidened){
            let values = dev.attr('class').split(' ');
            values.remove('hidden');
            dev.attr('class',values.join(' '));
            hidened = false;
        }else if(top < 600){
            let values = dev.attr('class').split(' ');
            values.remove('hidden').push('hidden');
            dev.attr('class',values.join(' '));
            hidened = true;
        }
    }

    window.addEventListener('scroll',(e)=>{
        checkDev();
    })
    
})

var ScrollPos = function(){
    // 浏览器适配
    return {
        left: window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft || 0,
        top: window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0
    };
}

Array.prototype.remove = function(...args){
    while(args.length > 1){
        this.removes(args.pop());
    }
    let index = this.indexOf(args[0]);
    while(index > -1){
        this.splice(index, 1);
        index = this.indexOf(args[0]);
    }
    return this; // 影响本身，建议复制
}
String.prototype.decode = function(){
    if (this.length === 0) {
        return this;
    }
    let s = this;
    s = s.replace(/&amp;/g, "&");
    s = s.replace(/&lt;/g, "<");
    s = s.replace(/&gt;/g, ">");
    s = s.replace(/&nbsp;/g, " ");
    s = s.replace(/'/g, "\'");
    s = s.replace(/&quot;/g, "\"");
    return s;
}
