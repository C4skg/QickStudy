window.onload = function(){
    'use strict';
    changeMode();
    $(".change").click(function(){
        var mode = isDark() ? '' : 'dark';
        changeMode(mode,this);
    })

    function changeMode(mode=null,btn=null){
        if(!mode && !btn){
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
                if (signal == 'true'){
                    let values = element.attr('class').split(' ');
                    values.remove('bg-dark','text-light');
                    if(mode == 'dark'){
                        values.push('bg-dark','text-light');
                    }
                    element.attr('class',values.join(' '));
                }
            }
        }
        // 按钮
        if(btn){
            var children = $(btn).children('i');
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

    function isDark(){
        var n_mode = !!($('html').attr('data-user-color-scheme'));
        var dark = localStorage.getItem('dark');
        console.log(typeof dark);
        if( dark == 'true' || n_mode){
            return true;
        }else{
            return false;
        }
    }
}