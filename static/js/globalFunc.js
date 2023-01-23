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
    // return this; //会影响本身，建议复制
}