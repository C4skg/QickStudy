import markdown,os;
import ColorOut as out;


def md2html(md:str):
    '''
        @effect: md code to html code;

        @param: md;type<str>;markdown code;

        @return type<str>; return html text
    '''

    exts = [
        'markdown.extensions.extra', 
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.toc',
        'markdown.extensions.fenced_code',
        ]
    
    html = '''
            <html lang="zh-cn">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <meta content="text/html; charset=utf-8" http-equiv="content-type" />
            </head>
            <body>
            %s
            </body>
            </html>
        '''
    ret =  markdown.markdown(md,extensions=exts);

    return str(html % ret);
    

def md2HtmlFile(md_file:str,out_path = ''):
    '''
        @effect: make md to html and write in <filename>

        @param: md;type<str>;markdown code;
        @param2: filename;type<str>;target file name;

        @return type<int>; 1 is success; 0 is faild;
    '''
    if not os.access(md_file,os.X_OK):
        return 0;
        
    with open(md_file,'rb') as mdF:
        md = mdF.read().decode();
    html = md2html(md);
    outfile = os.path.join(str(out_path) + "/" + md_file);
    try:
        with open( outfile ,'w', encoding='utf-8') as nHTML:
            nHTML.write(html);
        return 1;
    except:
        out.error("write to %s failed" % md_file);
        return 0;