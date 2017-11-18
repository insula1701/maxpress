from mistune import Markdown
from six import StringIO
import premailer, lesscpy
import os, re, json
from os.path import join as join_path


# 处理配置文件
def import_config(file='config.json'):
    with open(file, encoding='utf-8') as json_file:
        text = json_file.read()
        json_text = re.search(r'\{[\s\S]*\}', text).group()  # 去除json文件中的注释
    config = json.loads(json_text)
    cfg_lines = ['@{}: {};\n'.format(key, value)
                 for key, value in config.items() if not key == 'poster_url']
    with open(join_path('less', 'vars.less'), 'w', encoding='utf-8') as less_file:
        less_file.writelines(cfg_lines)
    return config


# 解析less文件，生成默认样式表
def compile_styles(file=join_path('less', 'default.less')):
    with open(file, encoding='utf-8') as raw_file:
        raw_text = raw_file.read()

    css = lesscpy.compile(StringIO(raw_text))
    with open(join_path('css', 'default.css'), 'w', encoding='utf-8') as css_file:
        css_file.write(css)


# 将待解析的md文档转换为适合微信编辑器的html
def md2html(text, styles=None, poster=''):
    md = Markdown()
    inner_html = md(text)
    result = premailer.transform(pack_html(inner_html, styles, poster))
    return result

def pack_html(html, styles=None, poster=''):
    if not styles: styles = [join_path('css/','default.css')]
    styles.append(join_path('css/','custom.css'))
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
            input('提示：运行前请将所有要转换的Markdown文档放入workspace/md目录中\n'
                  '请按回车键退出程序：')

    return wrapper


# 转换md目录（不包括嵌套目录）下的所有md文档
@report_error
def convert_all(src=join_path('workspace', 'md'), dst=join_path('workspace', 'html'),
                archive=True, styles=None):  # 通过styles参数传入css文件名列表时，默认样式将失效

    print('正在导入配置文件...', end=' ')
    config = import_config()
    print('导入成功!')

    if not styles:
        print('正在编译CSS样式表...', end=' ')
        compile_styles()
        print('编译成功!')
    elif isinstance(styles, str): styles = [styles]

    for file in os.listdir(src):

        if file.endswith('.md'):
            print('正在转换{}...'.format(file), end=' ')
            with open(join_path(src, file), encoding='utf-8') as md_file:
                text = md_file.read()
            result = md2html(text, styles, poster=config['poster_url'])

            with open(join_path(dst, file[:-3] + '.html'),
                      'w', encoding='utf-8') as html_file:
                html_file.write(result)
            print('转换成功！')

            if archive:
                print('正在存档{}...'.format(file), end=' ')
                archive_path = join_path('workspace', 'archive')
                if not os.path.exists(archive_path): os.mkdir(archive_path)
                os.rename(join_path(src, file), join_path(archive_path, file))
                print('存档成功!')

    print('\n请进入workspace／html目录查看所有生成的HTML文档')
    print('请进入workspace／archive目录查看所有存档的Markdown文档')


if __name__ == '__main__':

    # 全部转换并存档
    # convert_all()

    # 只转换不存档
    convert_all(archive=False)





