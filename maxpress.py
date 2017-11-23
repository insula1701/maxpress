from mistune import Markdown
from six import StringIO
import premailer, lesscpy
import sys, os, re, json
from os.path import join as join_path


ROOT = os.path.dirname(sys.argv[0])


# 处理配置文件
def import_config(file=join_path(ROOT, 'config.json')):
    with open(file, encoding='utf-8') as json_file:
        text = json_file.read()
        json_text = re.search(r'\{[\s\S]*\}', text).group()  # 去除json文件中的注释
    config = json.loads(json_text)
    cfg_lines = ['@{}: {};\n'.format(key, value)
                 for key, value in config.items() if not key == 'poster_url']
    variables = '\n'.join(cfg_lines) + '\n\n'
    with open(join_path(ROOT, 'less', 'styles.less'), encoding='utf-8') as styles_file:
        styles = styles_file.read()
    with open(join_path(ROOT, 'less', 'default.less'), 'w', encoding='utf-8') as default_less:
        default_less.write(variables + styles)
    return config


# 解析less文件，生成默认样式表
def compile_styles(file=join_path(ROOT, 'less', 'default.less')):
    with open(file, encoding='utf-8') as raw_file:
        raw_text = raw_file.read()

    css = lesscpy.compile(StringIO(raw_text))
    with open(join_path(ROOT, 'css', 'default.css'), 'w', encoding='utf-8') as css_file:
        css_file.write(css)


# 将待解析的md文档转换为适合微信编辑器的html
def md2html(text, styles=None, poster=''):
    md = Markdown()
    inner_html = md(text)
    result = premailer.transform(pack_html(inner_html, styles, poster))
    return result

def pack_html(html, styles=None, poster=''):
    if not styles: styles = [join_path(ROOT, 'css','default.css')]
    styles.append(join_path(ROOT, 'css','custom.css'))
    style_tags = ['<link rel="stylesheet" type="text/css" href="{}">'.format(sheet)
         for sheet in styles]

    if len(poster.strip()) > 0:
        poster_tag = '\n<br>\n<img src="{}" alt="poster"／'.format(poster)
    else: poster_tag = ''

    head = """<!DOCTYPE html><html lang="zh-cn">
          <head>
          <meta charset="UTF-8">
          <title>result</title>
          {styles}
          </head>
          <body>
          <div class="wrapper">\n""".format(styles='\n'.join(style_tags))

    foot = """{}\n</div>\n</body>\n</html>""".format(poster_tag)

    result = fix_tbl(fix_img(fix_li(head + html + foot)))
    return result

def fix_li(html):     # 修正粘贴到微信编辑器时列表格式丢失的问题
    result = re.sub(r'<li>([\s\S]*?)</li>',
                   r'<li><span>\1</span></li>', html)
    return result

def fix_img(html):    # 修正HTML图片大小自适应问题
    result = re.sub(r'(<p>)*?<img([\s\S]*?)>(</p>)*?',
                   r'<section class="img-wrapper"><img\2></section>', html)
    return result

def fix_tbl(html):    # 修正HTML表格左右留白问题
    result = re.sub(r'<table>([\s\S]*?)</table>',
                   r'<section class="tbl-wrapper"><table>\1</table></section>', html)
    return result


# 装饰器：提供报错功能
def report_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print('错误: {}'.format(e))
            input('提示：运行前请将所有要转换的Markdown文档放入temp目录中\n'
                  '请按回车键退出程序：')

    return wrapper

# 用于处理嵌套目录
def recursive_listdir(dir):
    for root, subdirs, files in os.walk(dir):
        for file in files:
            yield (file, join_path(root, file))

# 用于处理冲突的文件名
def autoname(defaultpath):
    ext = re.search(r'\..+?$', defaultpath).group()
    count = 0
    while count < 10000:
        suffix = '(%d)' % count if count > 0 else ''
        newpath = defaultpath[:0 - len(ext)] + suffix + ext
        if not os.path.exists(newpath):
            return newpath
        else:
            count += 1; pass


# 转换temp下的所有md文档
@report_error
def convert_all(src=join_path(ROOT, 'temp'),
                dst=join_path(ROOT, 'result', 'html'),
                archive=True, styles=None):  # 通过styles参数传入css文件名列表时，默认样式将失效

    print('[+] 正在导入配置文件...', end=' ')
    config = import_config()
    print('导入成功')

    if not styles:
        print('[+] 正在编译CSS样式表...', end=' ')
        compile_styles()
        print('编译成功')
    elif isinstance(styles, str): styles = [styles]

    for file, filepath in recursive_listdir(src):

        if file.endswith('.md'):
            print('[+] 正在转换{}...'.format(file), end=' ')
            with open(filepath, encoding='utf-8') as md_file:
                text = md_file.read()
            result = md2html(text, styles, poster=config['poster_url'])
            htmlpath = autoname(join_path(dst, file[:-3] + '.html'))
            with open(htmlpath,'w', encoding='utf-8') as html_file:
                html_file.write(result)
            print('转换成功[{}]'.format(htmlpath.split('/')[-1]))

            if archive:
                print('[+] 正在存档{}...'.format(file), end=' ')
                arch_dir = join_path(ROOT, 'result', 'archive')
                if not os.path.exists(arch_dir): os.mkdir(arch_dir)
                archpath = autoname(join_path(arch_dir, file))
                os.rename(filepath, archpath)
                print('存档成功[{}]'.format(archpath.split('/')[-1]))

    print('\n[+] 请进入result／html查看所有生成的HTML文档')
    print('[+] 请进入result／archive查看所有存档的Markdown文档')


if __name__ == '__main__':

    # 全部转换并存档
    convert_all()

    # 只转换不存档
    # convert_all(archive=False)





