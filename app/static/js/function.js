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
