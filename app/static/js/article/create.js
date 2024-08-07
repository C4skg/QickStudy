function titleCount(){
    let input = $(".title input"),
        label = $(".title label");
    let len = input.val().length
    label.html(
        `${len}/100`
    )
    let color = (len > 100 || len == 0) ? "red" : "var(--border-color)";
    // input.css('border-color',`${color}`)
    label.css('color',color)
    window.title = Boolean(
        len < 100 && len != 0
    )
}
//set Cover image
var setCover = function(){
    let status = $(".extend .fm").attr('data-status');
    if(status == "normal"){
        document.getElementById('cover').click();
    }
}
window.title = false;
window.cover = false;
$(function(){
    var mode = window.mode || 'light';
    window.vditor = new Vditor("vditor", {
        cache: {
            enable: true
        },
        // width: ,
        height: document.body.offsetHeight,
        tab: '  ',
        cdn: '/static/Vditor',
        mode: 'wysiwyg',
        counter: {
            enable: true
        },
        // *主题设置
        theme: mode,
        hint:{
            parse: false
        },
        outline:{
            enable: true
        },
        preview:{
            hljs:{
                enable:true,
                style: mode=='dark'?'native':'emacs',  //emacs, dark:native
                lineNumber: true
            },
            math:{
                engine: "KaTeX",
                inlineDigit: true
            },
            theme:{
                current: mode
            }

        },
        cache:{
            enable: false
        },
        upload:{
            url: window.upload.editor,
            accept: 'image/*',
            max: 5 * 1024 * 1024,
            extraData: {
                'csrf_token': window.csrf_token
            },
            fieldName: 'file', 
            format:function(files,res){
                res = JSON.parse(res);
                var result = {
                    code: 0,
                    data: {
                        errFiles: [],
                        succMap: {
                        } 
                    },
                };
                for(let sf of res.files){
                    if(sf.status == 'success'){
                        result.data.succMap[sf.filename] = sf.path
                    }else{
                        result.data.errFiles.push(
                            sf.filename
                        )
                    }
                }
                return JSON.stringify(result);
            },
            error: function(e){
                window.extends.tips.create("上传失败",window.extends.tips.type.danger)
            }
        },
        after(){
            let ready = document.getElementById("ready");
            if(ready){
                const context = ready.innerHTML;
                ready.remove();
                if(context && context.length > 0){
                    window.vditor.setValue(
                        context.decode()
                    )
                }
            }
            
            

        },
        input(value){
            try{
                realTimeSaveContext(value);
            }catch{
                console.error("real time save error");
            }
        },
        toolbar: ['emoji' , 'headings' , 'bold' , 'italic' , 'strike' , '|' , 'line' , 'quote' , 'list' , 'ordered-list' , 'check' ,'outdent' ,'indent' , 'code' , 'inline-code' , 'insert-after' , 'insert-before' ,'undo' , 'redo' , 'upload' , 'link' , 'table' , 'fullscreen' , 'outline', 'devtools','|','both','edit-mode','export' , 'help',
            {
                hotkey: '⌘S', //Ctrl + s
                name: 'save',
                tip: '保存',
                className: '',
                icon: '<svg t="1689558431701" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1464" width="200" height="200"><path d="M845.312 0.512H32.512v1022.976h958.976v-876.8L845.312 0.512z m-172.864 62.976v256H351.488v-256h320.96zM287.488 960.512V605.76l29.184-29.248h390.656l29.184 29.248v354.752H287.488z m640 0h-126.976V585.152L727.424 512H296.576L223.488 585.152v375.36H96.512V63.488h190.976v320.448h449.024V63.488h79.68l111.296 112.32v784.704z m-384-832h65.984v128H543.488v-128z" p-id="1465" fill="#666"></path></svg>',
                click () {
                    window.extends.tips.create("保存成功",window.extends.tips.type.success)
                },
            }
        ],
        hint:{
            extend:[
                {
                    key: "@",
                    hint: (key)=>{
                        return [
                            {
                                value: `> 作者: \`<${window.user.username}>\``,
                                html: `插入作者:<img src='${window.user.logo}'/> ${window.user.username}`
                            }
                        ]
                    }
                },
                {
                    key: "!",
                    hint: (key)=>{
                        return [
                            {
                                value: '![]()',
                                html: '插入图片'
                            }
                        ]
                    }
                }
            ]
        }
    });
    Object.defineProperty(window,"mode",{
        set: function(value){
            window.location.reload();
        }
    });    

    //cover upload
    const input = $("#cover")[0];
    input.addEventListener('change',function(){
        $(".extend .fm").attr('data-status','waiting');
        var formData = new FormData();
        formData.append('csrf_token',window.csrf_token)
        formData.append('file',input.files[0])
        formData.append('articleId',window.article.id)
        $.ajax({
            url: window.upload.cover,
            type: "post",
            processData: false,
            contentType: false,
            data: formData,
            success: (e)=>{
                if(typeof e === String){
                    e = JSON.parse(e)
                }
                if(e['status']=='success'){
                    $('.extend .fm').attr('data-status','success')
                    $('.extend .fm').attr('data-desc','上传成功')
                    setTimeout(()=>{
                        let img = $('.extend picture img')[0]
                        img.src = e['files'][0]['path'];
                    },1000)
                    
                }else{
                    $('.extend .fm').attr('data-status','error')
                    $('.extend .fm').attr('data-desc','上传失败')
                    input.value=''
                }
            },
            error:(e)=>{
                $('.extend .fm').attr('data-status','error')
                $('.extend .fm').attr('data-desc','上传失败')
                input.value=''
            },
            complete:(e)=>{
                setTimeout(()=>{
                    $('.extend .fm').attr('data-status','normal')
                    $('.extend .fm').attr('data-desc','设置封面')
                },1000)
            }
        })
    });
})
//when leave
var beforeunload = function(e){
    e.preventDefault();
    e.returnValue = ''
}
window.addEventListener('beforeunload',beforeunload)

//save
var save = function(type){
    titleCount();
    if(!window.title){
        return false;
    }
    const title = $(".title input").val(),
          typeId = $("#ArtType").val();
    var context = "";
    try{
        context = window.vditor.getValue();
    }catch{
        context = "";
    }
    if(context.length == 0){
        window.extends.tips.create("请输入文章内容！",window.extends.tips.type.danger)
        return false;
    }
    var form = new FormData();
    form.append('title',title)
    form.append('context',context)
    form.append('csrf_token',window.csrf_token)
    form.append('tId',type)
    form.append('typeId',typeId)
    form.append('id',window.article.id)
    $.ajax({
        url : window.upload.save,
        processData: false,
        contentType: false,
        type: 'post',
        data: form,
        success: (e)=>{
            if(e['status']=='success'){
                swal("成功！","文章已保存", "success").then(()=>{
                    window.removeEventListener('beforeunload',beforeunload)
                    window.location = e['route']
                    // window.location.reload();
                })
            }else{
                swal("失败",e['message'], "error").then(()=>{
                    
                })
            }
        },
        error: (e)=>{
            swal('失败','网络错误','error');
        },
        complete: (e)=>{

        }
    })
}

// article context with real time save
var realTimeSaveContext = function(value){
    var form = new FormData();
    var context = value;
    if(context.length == 0){
        window.extends.tips.create("请输入文章内容！",window.extends.tips.type.danger)
        return false;
    }
    form.append('context',context)
    form.append('csrf_token',window.csrf_token)
    form.append('id',window.article.id)
    $.ajax({
        url : window.upload.save,
        processData: false,
        contentType: false,
        type: 'post',
        data: form,
        success: (e)=>{
            if(e['status']=='success'){
                window.extends.tips.create("保存成功",window.extends.tips.type.success)
            }else{
                window.extends.tips.create("保存失败",window.extends.tips.type.danger)
            }
        },
        error: (e)=>{
            window.extends.tips.create("保存失败",window.extends.tips.type.danger)
        },
        complete: (e)=>{

        }
    })
}