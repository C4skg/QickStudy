window.onload = function(){
    'use strict';
    // 运行时检查
    (function(){
        changeMode();
        checkDev();

        //
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl)
        })
    })();

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
            console.log(mode)
        }else{
            localStorage.setItem('dark',mode == 'dark');  
        }
        var node = $("*");
        if(mode == 'dark'){
            $('html').attr('data-user-color-scheme','1')
        }else{
            $('html').removeAttr('data-user-color-scheme')
        }
        for(let element of node){
            if(typeof(element) === "object"){
                element = $(element);
                let signal = element.attr('data-dark-change');
                if (signal){
                    signal = String(signal).split(';');
                    let values = element.attr('class').split(' ');
                    values.remove('bg-dark','text-light');
                    if(mode == 'dark'){
                        if(signal.includes("color")){
                            values.push('text-light');
                        }else if(signal.includes("back")){
                            values.push('bg-dark');
                        }
                    }
                    element.attr('class',values.join(' '));
                }
            }
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
    }

    function isDark(){
        var dark = localStorage.getItem('dark');
        console.log(typeof dark);
        if( dark == 'true'){
            return true;
        }else{
            return false;
        }
    }

    function checkDev(){
        let top = ScrollPos().top,
            hidened = true;
        let dev = $('.rightbottom');
        if(dev.length == 0) return;
        if(top >= 1000 && hidened){
            let values = dev.attr('class').split(' ');
            values.remove('hidden');
            dev.attr('class',values.join(' '));
            hidened = false;
        }else if(top < 1000){
            let values = dev.attr('class').split(' ');
            values.remove('hidden').push('hidden');
            dev.attr('class',values.join(' '));
            hidened = true;
        }
    }

    window.addEventListener('scroll',(e)=>{
        checkDev();
    })
    
}

var ScrollPos = function(){
    // 浏览器适配
    return {
        left: window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft || 0,
        top: window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0
    };
}

Array.prototype.remove = function(...argv){
    if(argv.length > 1){
        argv.forEach(element => {
            this.remove(element);
        });
    }
    let index = this.indexOf(argv[0]);
    while(index > -1){
        this.splice(index,1);
        index = this.indexOf(argv[0]);
    }
    return this; //会影响本身，建议复制
}