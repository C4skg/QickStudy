window.onload = function(){
    'use strict';
    $(".change").click(function(){
        var mode = isDark() ? '' : 'dark';
        changeMode(mode,this)
    })

    function changeMode(mode,btn){
        var url = new URL(document.URL)
        $.ajax({
            url: url.origin + '/api',
            type: 'POST',
            data: `style=${mode}`,
            success: function(r){
                console.log(r)
            }
        })
        var node = $("*");
        for(let element of node){
            if(typeof(element) === "object"){
                element = $(element);
                let signal = element.attr('data-dark-change');
                if (signal == 'true'){
                    let values = element.attr('class').split(' ');
                    values.remove('bg-dark','text-light');
                    if(mode == 'dark'){
                        values.push('bg-dark','text-light');
                        $('html').attr('data-user-color-scheme','1')
                    }else{
                        $('html').removeAttr('data-user-color-scheme')
                    }
                    element.attr('class',values.join(' '));
                }
            }
        }
        // 按钮
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

    function isDark(){
        var n_mode = $('html').attr('data-user-color-scheme');
        return !!(n_mode)
    }
}