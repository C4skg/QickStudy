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
                console.log(e);
                for(let id in e){
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
                        article.detailPath
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

    function generateArticleCard(title,context,userimgPath,username,lasttime,agreenum,watchnum,coverPath,detailPath){
        var card = $(`
        <div class="card">
            <div class="p-2">
                <div class="aBody">
                    <div class="cover ${coverPath == null ? 'hidden' : ''}">
                        <img src="${coverPath}" alt="">
                    </div>
                    <div class="main" data-max='true'>
                        <div class="title">
                            <a href="${detailPath}" target="_blank" data-bs-toggle="tooltip" title="${title}" >${title}</a>
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
                                        ${username}
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
