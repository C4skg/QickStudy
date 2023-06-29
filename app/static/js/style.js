$(function(){
    'use strict';
    // while runtime
    (function(doc,win){
        changeMode();
        checkDev();
        topNotice();
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
        //!imgChange
        var img = $('img');
        for(let i of img){
            if ($(i).attr('data-mode-change') != 'true'){
                continue;
            }
            let src = i.src.split('\/'),
                filename = src[src.length-1].split('.')
            if(mode == 'dark'){
                filename[0] = filename[0].split('-')[0]
            }else{
                filename[0] += '-dark';
            }
            src[src.length - 1] = filename.join('.')
            i.src=src.join('\/')
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

    // 置顶公告
    function topNotice(){
        let accordion = $('.accordion'),
            children = accordion.children();
        accordion.empty();
        let ready = []
        for(let card of children){
            ready.push(card)
        }
        ready.sort(
            (a,b)=>{
                let a1 = parseInt($(a).attr('data-level')) || -1,
                    b1 = parseInt($(b).attr('data-level')) || -1;
                return (a1<b1)-(b1<a1)  //! 修复 chrome sort 问题
            }
        )
        // console.log(ready);
        accordion.append(
           ready 
        )
    }
})

var ScrollPos = function(){
    // 浏览器适配
    return {
        left: window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft || 0,
        top: window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0
    };
}