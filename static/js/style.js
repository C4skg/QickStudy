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
                var children = $(eve).children('img');
                for(let child of children){
                    let jQChild = $(child);
                    let attr = jQChild.attr('src');
                    if(mode == 'dark'){
                        attr = attr.replace('sun.png','moon.png')
                    }else{
                        attr = attr.replace('moon.png','sun.png')
                    }
                    jQChild.attr('src',attr)
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