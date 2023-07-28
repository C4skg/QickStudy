Array.prototype.remove = function(...args){
    while(args.length > 1){
        this.remove(args.pop());
    }
    let index = this.indexOf(args[0]);
    while(index > -1){
        this.splice(index, 1);
        index = this.indexOf(args[0]);
    }
    return this; // 影响本身，建议复制
}
String.prototype.decode = function(){
    if (this.length === 0) {
        return this;
    }
    let s = this;
    s = s.replace(/&amp;/g, "&");
    s = s.replace(/&lt;/g, "<");
    s = s.replace(/&gt;/g, ">");
    s = s.replace(/&nbsp;/g, " ");
    s = s.replace(/'/g, "\'");
    s = s.replace(/&quot;/g, "\"");
    return s;
}
String.prototype.removeBlankLines = function () {
    return this.replace(/(\n[\s\t]*\r*\n)/g, '\n').replace(/^[\n\r\n\t]*|[\n\r\n\t]*$/g, '')
}
window.extends = {}
var tips = {
    id: "extends__tips__",
    timeout: 2000,
    type: {
        success: 'success',
        info : 'info',
        warning: 'warning',
        danger: 'danger',
        primary: 'primary',
        secondary: 'secondary',
        light: 'light',
        dark: 'dark'
    },
    create: function(context,type){
        let body = document.getElementsByTagName('body')[0],
            _id = this.id + ((~~(Math.random() * (1<<24))).toString(16));
        let alerts = document.createElement('div');
        alerts.className = `alert col-sm-3 alert-${type}`
        alerts.id = _id
        alerts.setAttribute('style','position: absolute;bottom: 0;right: 0;z-index: 999999;');
        let text = document.createElement('strong');
        text.innerText = context;
        alerts.appendChild(
            text
        )
        body.appendChild(alerts)
        setTimeout(
            function(){
                document.getElementById(_id).remove();
            },
            this.timeout
        )
    }
}

window.extends.tips = tips;

window.ScrollPos = function(){
    // 浏览器适配
    return {
        left: window.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft || 0,
        top: window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || 0
    };
}