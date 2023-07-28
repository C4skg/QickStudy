var page = 1;
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
    })
    
    function getArticle(){
        $.ajax({
            url: window.server.getArticle,
            type: 'get',
            success: (e)=>{
                if(typeof e === 'string') e = JSON.parse(e);
                for(let id in e){
                    $('.context .NoneTxt').remove();
                    const article = e[id];
                    generateArticleCard(
                        article.title,
                        article.context,
                        article.auth.logo,
                        article.auth.username,
                        article.lasttime,
                        article.agree,
                        article.watch,
                        article.cover,
                        article.detailPath,
                        article.auth.url
                    )
                }
            },
            error: (e)=>{

            },
            complete: (e)=>{

            }
        })
        page++;
    }

    getArticle();

    function generateArticleCard(title,context,userimgPath,username,lasttime,agreenum,watchnum,coverPath,detailPath,authUrl){
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
                            ${context}
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
                                    <div class="item" data-num="${watchnum}">
                                        <span class="svg watch text-muted" data-num="123">
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
    }
})
