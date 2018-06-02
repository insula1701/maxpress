# MaxPress：MarkDown+Python实现微信公众号一键排版

-------------
更新针对非技术人员的小白教程：

**【上篇：基本原理】**[《懒人福音： 怎样做一个从不排版的微信小编？》](https://mp.weixin.qq.com/s?__biz=MzI2NjM5NDMyMw==&mid=2247483713&idx=1&sn=0ec80785ce60503eb30e4ce27ac89781&chksm=ea8f8efdddf807ebb5137b1f0d8c652bcaa33e861d2c0544b50aeed051361b904cf194f6f844)

**【下篇：语法指南】** [《微信公众号MarkDown排版完全指南》](https://mp.weixin.qq.com/s?__biz=MzI2NjM5NDMyMw==&mid=2247483712&idx=1&sn=e8c2c8e9478045e335033b84f12be46e&chksm=ea8f8efcddf807ea61ce72618e0d89dd755635108cb898bbe1c103fcf2a4a029dc629e35b87b)

-------------

## 基本功能

1. 批量转换MarkDown文档为适合粘贴微信编辑器的HTML文件。
2. 支持自定义：正文字号、文字颜色（正文颜色、主题色、引用色）、行间距、段间距、标题水平对齐方式、内容两侧留白比例、底部图片。
3. 转换完成的MarkDown文档可以自动移动存档。

## 开始使用

### 下载

[下载最新稳定版本：Windows版/Mac版](https://github.com/insula1701/maxpress/releases)

### 使用Windows/Mac版可执行程序

#### 一键排版

1. 使用Markdown创作你的内容，保存为`.md`文件，放入`temp`目录中。
2. 双击运行`maxpress`程序，`result／html`目录下将生成同名的`.html`文件。
3. 用浏览器打开生成的`.html`文件，全选复制，粘贴到微信编辑器中。
4. 检查，预览，调整。

**【注意事项】**

1. **推送前请务必发送到手机预览仔细检查，作者不为最终样式的绝对正确担保。**
2. **转换前请务必在软件目录之外留有原文档副本，作者不为意外发生的数据丢失负责。**
3. 目前只测试了Win/Mac上的**Chrome**浏览器，如果这一步出现格式丢失/错乱等情况，请在issue中反馈，说明你**遇到的问题、使用的系统和浏览器。**
4. 支持多个`.md`文件、多个子目录（包括嵌套子目录）的批量转换。
5. 默认进行自动存档，即转换完毕后将所有原始`.md`文件移动至`result／archive`目录下，可修改配置文件（auto_archive）禁用此功能。
6. 如果出现文件名冲突的情况，默认同文件名自动覆盖，可修改配置文件（auto_rename）改为进行自动重命名。


#### 格式调整

在运行转换程序之前，修改`config.json`文件，可自定义常用格式变量。

包括：

| 变量名 | 默认值 | 说明 |
| :----- | :----- | :---- |
|main_size     |16px   |正文主字号|
|theme_color   |#349971|主题色，用于标题、强调元素等文字颜色|
|text_color    |#555   |正文文字颜色|
|quote_color   |#999   |引用框和代码框内文字颜色|
|line_height   |2em    |正文行高|
|para_spacing  |1.5em  |正文段间距|
|align         |多项    |各部分的水平对齐方式，建议`left`或`center`（`h1`～`h6`代表标题1～标题6，`content`代表正文）|
|main_margin   |3%     |内容两侧留白比例|
|banner_url    |""     |文章头部引导关注图片的url|
|poster_url    |""     |底部二维码／海报图片的地址|
|convert_list  |true   |将正文中的列表转换为普通段落，以修正微信不能正常显示列表序号样式的问题（仅用于微信）|
|ul_style      |"○"    |将无序列表转换为普通段落后，每项之前的符号标识（仅当`convert_list`为`true`时启用）|
|auto_archive  |""     |是否自动存档（转换后将原始`.md`文件移动至`result／archive`目录下）|
|auto_rename   |false  |冲突文件名的处理：`true`自动重命名；`false`覆盖先前的文件|


**备注：**

- 如果对自定义的要求不高，建议更换一下`theme_color`，其余可以采用默认配置。
- 目前这版微信UI，貌似对所有列表序号都只能显示默认样式，即使把样式写进上级元素，粘贴进编辑器的时候也会被“洗掉”，目前尚未找到方法绕过此限制，因此添加`convert_list`选项作为临时解决方案，当此项为`true`时，正文中的所有列表（不包括代码块中的内容）会被转化为段首带序号的普通段落。注意，这种情况下，`styles.less`中专门为列表设置的样式将会失效。如果你有更好的办法，欢迎开issue告诉我。


#### 更多自定义

如果你希望覆盖默认样式中的个别样式，可以自主编写`custom.css`，它将在`default.css`之后被引入。

#### 示例

[`example.md`](https://github.com/insula1701/maxpress/blob/master/temp/example.md) -> 
[`example.html`](https://github.com/insula1701/maxpress/blob/master/result/html) （html请下载后在浏览器中打开）

公众号文章示例：[微信公众号MarkDown排版完全指南](https://mp.weixin.qq.com/s?__biz=MzI2NjM5NDMyMw==&mid=100000048&idx=1&sn=7bb0a7fd4cd92ed6b753e996e7eaf0ce&chksm=6a8f8e8c5df8079af7324b2505670d2abd0e83552873fcdaf7acf52ae8b25399380d60a5d778&mpshare=1&scene=1&srcid=1229tvTWQ1h4dDLJEYny9An8&key=dd3ea87ce1ad0714eaba7dea68d348c20f5b3fb8317e722240f1ef78c7894661ea5fdd718290986a650fdf3b2dd72762d7f4afd75e91ed2a0c7731a2a687388c964eb644526833a72f511f019b2ccb21&ascene=0&uin=MjE0NzM5NTU4MQ%3D%3D&devicetype=iMac+MacBookPro12%2C1+OSX+OSX+10.12.4+build(16E195)&version=12020810&nettype=WIFI&lang=zh_CN&fontScale=100&pass_ticket=6iRWB3aLBCQOXpS5n6I%2BNeH5AK3ygPJiPOMvcoNPo5bULSUy%2BHV4uZXOUJKw3n%2FK)

### 使用Python脚本【推荐】

如果你的计算机上装有Python环境，可以直接运行脚本。建议从Master分支获取最新稳定版本。

#### 开发环境

使用Python 3.5.2开发，CSS样式表使用LESS编译。建议在Python 3环境下使用。

依赖的包：[mistune](https://github.com/lepture/mistune)，
[premailer](https://github.com/peterbe/premailer)，
[lesscpy](https://github.com/lesscpy/lesscpy)

快速安装依赖：`pip install -r requirements.txt`

#### 运行

直接运行：`python maxpress.py`

或者作为模块导入：

```
import maxpress

maxpress.convert_all(archive=True, styles=None)
```
如果你希望整体弃用默认样式并启用自定义CSS样式表，可以通过`styles`参数传入自定义CSS文件路径（支持用列表传入多个），这时`config.json`中用于定义样式的参数将会失效，`custom.css`将在你的全部自定义样式表之后引入。

带样式的列表粘贴到微信编辑器时，可能意外出现格式丢失的情况（貌似是微信的bug？），目前通过在每个`li`元素内额外添加一个`span`元素包装样式，暂时可以解决。但要注意，如果自定义样式的话，为`li span`所设置的字号、颜色等不能与上级元素完全一致，否则在粘贴到微信编辑器时会被自动去掉。

## 示例

[`example.md`](https://github.com/insula1701/maxpress/blob/master/temp/example.md) -> 
[`example.html`](https://github.com/insula1701/maxpress/blob/master/result/html) （html请下载后在浏览器中打开）

## 后续开发计划

- [x] 可选在文首自动添加引导关注Banner
- [ ] 代码的精简&重构（不影响功能）
- [ ] 支持更多样化的文中小标题模式配置
- [ ] 支持Hexo博客文章的直接转换
- [ ] 简化HTML及CSS自定义流程

## Reference

设计思路及部分默认样式参考了：
 - [可能吧公众号的文章是如何排版的？](https://kenengba.com/post/3507.html)
 - 李笑来[`markdownhere.css`](https://gist.github.com/xiaolai/aa190255b7dde302d10208ae247fc9f2)
 - [MDPUB](http://md.codingpy.com/)

## License

MIT