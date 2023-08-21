window.page = 1;
var loadSignal = false;
var over = false;
$(function(){
    window.addEventListener('scroll',(e)=>{
        let pos = window.ScrollPos();
        if(pos.top >= 100){
            $('.rightContainer').css({
                'left': 0,
                'top': pos.top - 100
            })
        }else{
            $('.rightContainer').css({
                'left': 0,
                'top': 0
            })
        }

        //lazyloading
        
        if(pos.top + window.innerHeight >= (document.body.scrollHeight - 100)){
            // allow load
            if(loadSignal || over) return false;

            loadSignal = true
            $(".main .detail").append('<div id="_lazyload" style="text-align:center;padding: 50px 0;"><span class="spinner-border spinner-border-sm"></span></div>');
            getArticle()
        }
    })
    
    function getArticle(){
        $.ajax({
            url: window.server.getArticle,
            type: 'get',
            data: {
                "page": window.page
            },
            success: (e)=>{
                if(typeof e === 'string') e = JSON.parse(e);
                if(e['length'] > 0){
                    window.page++;
                    let articleList = e['articles'];
                    for(let id in articleList){
                        $('.context .NoneTxt').remove();
                        const article = articleList[id];
                        generateArticleCard(
                            article.title,
                            article.context,
                            article.auth.logo,
                            article.auth.username,
                            article.lasttime,
                            article.agree,
                            article.comments,
                            article.cover,
                            article.detailPath,
                            article.auth.url
                        )
                    }
                }else{
                    over = true;
                }
            },
            error: (e)=>{
                over = true;
            },
            complete: (e)=>{
                loadSignal = false;
                $('#_lazyload').remove();
            }
        })
    }

    getArticle();

    function generateArticleCard(title,context,userimgPath,username,lasttime,agreenum,comments,coverPath,detailPath,authUrl){
        Vditor.md2html(
            context,
            {
                cdn: '/static/Vditor'
            }
        ).then(function(html){
            html = filterXSS($(html).text());
            var card = $(`
            <div class="card">
                <div class="p-2">
                    <div class="aBody">
                        ${coverPath == null ? '' : 
                        `   <div class="cover">
                                <img src="${coverPath}" alt="">
                            </div>
                        `
                        }
                        <div class="main" data-max='${coverPath ? '' : 'true'}'>
                            <div class="title">
                                <a href="${detailPath}" target="_blank">${title}</a>
                            </div>
                            <div class="contextDept text-muted">
                                ${html}
                            </div>
                            <div class="extends">
                                <div class="userinfo">
                                    <div class="logo">
                                        <img src="${userimgPath}" class="rounded-circle" alt="">
                                    </div>
                                    <div class="username">
                                        <span class="username text-muted">
                                            <a href="${authUrl}" target="_blank">${username}</a>
                                        </span>
                                    </div>
                                </div>
                                <div class="articleInfo text-muted">
                                    <div class="step">
                                        <div class="item">
                                            <span class="svg time">
                                                ${window.icon.time}
                                            </span>
                                            ${lasttime}
                                        </div>
                                    </div>
                                    <div class="step">
                                        <div class="item" data-num="${agreenum}">
                                            <span class="svg agree text-muted" >
                                                ${window.icon.agree}
                                            </span>
                                        </div>
                                        <div class="item" data-num="${comments}">
                                            <span class="svg watch text-muted">
                                                ${window.icon.watch}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            `)
            $(".main .detail").append(card);
        })        
    }
})
