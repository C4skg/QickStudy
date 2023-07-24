function titleCount(){
    let input = $(".title input"),
        label = $(".title label");
    let len = input.val().length
    label.html(
        `${len}/100`
    )
    label.css('color',len > 100 ? "red" : "var(--border-color)")
}
$(function(){
    var mode = window.mode || 'light';
    var vditor = new Vditor("vditor", {
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
        upload:{
            url: window.upload_url,
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
            // console.log(vditor.getHTML())
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
    })
    
    //release
    document.getElementById('release').onclick = function(){
        const input = $(".SubmitForm")
        console.log(
            input.serialize()
        )
    }

})