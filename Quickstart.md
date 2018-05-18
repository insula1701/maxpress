# 快速上手

## 一键排版

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

## 格式调整

在运行转换程序之前，修改`config.json`文件，可自定义常用格式变量。

包括：


| 变量名 | 默认值 | 说明 |
| :----- | :----- | :---- |
|main_size     |16px   |正文主字号|
|theme_color   |#02ccba|主题色，用于标题、强调元素等文字颜色|
|text_color    |#555   |正文文字颜色|
|quote_color   |#999   |引用框和代码框内文字颜色|
|line_height   |2em    |正文行高|
|para_spacing  |1.5em  |正文段间距|
|align         |多项    |各部分的水平对齐方式，建议`left`或`center`（`h1`～`h6`代表标题1～标题6，`content`代表正文）|
|main_margin   |3%     |内容两侧留白比例|
|poster_url    |""     |底部二维码／海报图片的地址|
|auto_archive  |""     |是否自动存档（转换后将原始`.md`文件移动至`result／archive`目录下）|
|auto_rename   |false  |冲突文件名的处理：`true`自动重命名；`false`覆盖先前的文件|

## 更多自定义

如果你希望覆盖默认样式中的个别样式，可以自主编写`custom.css`，它将在`default.css`之后被引入。

## 示例&更多用法参考

[《懒人福音： 怎样做一个从不排版的微信小编？》](https://mp.weixin.qq.com/s?__biz=MzI2NjM5NDMyMw==&mid=2247483713&idx=1&sn=0ec80785ce60503eb30e4ce27ac89781&chksm=ea8f8efdddf807ebb5137b1f0d8c652bcaa33e861d2c0544b50aeed051361b904cf194f6f844)

[《微信公众号MarkDown排版完全指南》](https://mp.weixin.qq.com/s?__biz=MzI2NjM5NDMyMw==&mid=2247483712&idx=1&sn=e8c2c8e9478045e335033b84f12be46e&chksm=ea8f8efcddf807ea61ce72618e0d89dd755635108cb898bbe1c103fcf2a4a029dc629e35b87b)
