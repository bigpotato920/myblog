Title: 用pelican和gitpages搭建博客
Date: 2014-2-15
Modified: 2014-2-15
Category: tools
Tags: 静态网站生成器, pelican, github, python
Slug: pelcian_blog
Summary: 利用pelican生成静态网站，在github上进行托管
Author: bigpotato

## 用pelican和gitpages搭建博客
一直以来都想自己搭建一个博客，对平时学习的点滴进行记录，苦于一直没空，最近放假开始着手进行，折腾了 几天总算有点眉目，现在记录下搭建博客的整个过程算是对这几天折腾的一个总结，顺便能给后来人一些经验，少一些无谓的折腾。


搭建博客之前也在网上搜集了写资料，发现这种静态网站生成器很多，而且许多工具像wordpress这种已经做的相当自动化，门槛很低；还有Jekyll、Octopress基于ruby的网站生成器用于也很多，但苦于不会php，ruby也懒得去学，最终找到一款基于python的网站生成器pelican，其网站模板是用Flask的默认模板语言Jinja2，以前有过学习。


学习新东西的通用思路，打开google找到pelican的项目主页浏览它的官方教程。这里要说的是其实学习工具类的东西最好还是去官网，因为随着工具的升级，以前的方法可能就不再适用，而官网会对教程做持续性更新，是最权威的。由于pelcian的安装，博客的编写，博客本地的预览等部分[官网的教程][]写的已经很详细而且也比较简单，这里就不在赘述。


1.博客样式设置


这里说说博客主题的设置，当用pelcian生成网站后需要自己安装相应的主题来对网站界面进行美化，我选择[pelican-bootstrap3][]作为我博客的主题。在github上下载主题后，在pelican生成的网站的pelicanconf.py文件中设置主题的路径THEME = 'path of pelican-bootstrap3',重新生成网站后来本地便可以预览到主题的效果。对网站的默认字体不是很喜欢，这里进行自定义，下载[Lato][]作为英文的默认字体保存到`pelican-bootstrap3/static/fonts`下，并在style.css设置启用该字体

```css
@font-face {
    font-family: 'Lato';
    src: url('../fonts/Lato-Regular.ttf');
}
```
对中文字体修改
```css
h1,h2,h3,h4,h5,h6,.h1,.h2,.h3,.h4,.h5,.h6 {font-family: 'Microsoft YaHei', 微软雅黑, "Lato", sans-serif;}
p, a ,body {font-family: 'Microsoft YaHei', 微软雅黑, "Lato",  sans-serif;}
```
由于时常会在博文中插入代码，这里对代码块的样式进行了一些设置，首先把代码块的字体改成`Source Code Pro`, 对代码块增加行号。
```css
/* For use with the code_line-number_word-wrap_switcher_jquery.js Pelican plugin */
code {
    overflow: auto;
    /* This uses `white-space: pre-wrap` to get elements within <pre> tags to wrap. Python, for code chunks within three backticks (```), doesn't wordwrap code lines by default, because they're within <pre> tags, which don't wrap by default. See https://github.com/github/markup/issues/168 , which is specifically about this parsing issue, even though that link's discussion is talking about GitHub. */
    white-space: pre-wrap;       /* css-3 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
}

/* Following http://bililite.com/blog/2012/08/05/line-numbering-in-pre-elements/, use CSS to add line numbers to all spans that have the class 'code-line' */

.highlight pre {
    font-family: "Source Code Pro", monospace;
    counter-reset: linecounter;
    padding-left: 2em;
}
.highlight pre span.code-line {
    counter-increment: linecounter;
    padding-left: 1em;
    text-indent: -1em;
    display: inline-block;
}
.highlight pre span.code-line:before {
    content: counter(linecounter);
    padding-right: 1em;
    display: inline-block;
    color: grey;
    text-align: right;
}
```
这里并没有使用pygments默认的行号设置，markdown中代码生成有两种方式：1.用tab键缩进2.利用三个反引号标记。如果利用反引号标记后在第一行写入`#!python`则生成的代码块是有行号的，否则没有。但这种方式并不适用于shell脚本，因为shell脚本通常第一行都是`#! /bin/bash`这在markdown中是无法正常显示的，并且pygments生成的行号会在复制时被选择上。这里行号显示采用了pelcian的一个插件：[better_codeblock_line_numbering][],具体设置参见项目的README。

[pelican-bootstrap3]: https://github.com/DandyDev/pelican-bootstrap3
[Lato]: https://github.com/ForestWatchers/pelican-theme/blob/master/static/font/Lato-Regular.ttf
[better_codeblock_line_numbering]: https://github.com/getpelican/pelican-plugins/tree/master/better_codeblock_line_numbering


2.利用gitpages搭建博客


利用github的网站托管功能可以很容易的搭建博客，具体教程官网也有。最开始时我在github上建立了一个名为username.github.io的仓库，而后想在output目录下建立本地的仓库把output目录下的文件上传到github上，但尝试了几次后git老是不能push到github，让我检查这个代码仓库是否存在，几次都没成功后也没找到原因，后来选了退而求其次的方法，在本地clone远端github的username.github.io的空的仓库，然后把output目录下内容复制到username.github.io下push到github。然后在output目录下就能够正常更新了（感觉还是很蛋疼，有空查找下原因）。


3.启用Disqus评论


在pelican-bootstrap3下已经已经写好Disqus的网页，不用手工添加代码，只要在pelicanconf.py中启用Disqus即可。这里折腾了一天，正确的方式是先到[Disqus][]注册一个用户，然后注册一个网站的shortname，在https://yourshortname.disqus.com/admin/settings/general/进行一些常规设置，然后到https://yourshortname.disqus.com/admin/settings/advanced/下设置信任的域。最后到pelicanconf.py中设置

```python
#Disqus comments
SITEURL = u"your blog url"
DISQUS_SITENAME = u"your shortname"
# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False
```
注意这里一定要设置SITEURL，并且设置成绝对地址，否则Disqus就会报
>“We were unable to load Disqus. If you are a moderator please see our troubleshooting guide.”

的错误。不过这样也有一个缺点就是不能在本地正常预览了。

[Disqus]: https://disqus.com/

##参考文献
[1. http://docs.getpelican.com/en/3.5.0/index.html][1]
  

[2. https://github.com/DandyDev/pelican-bootstrap3][2]
  

[3. http://elfnor.com/pelican-and-markdown-styling-cheat-sheet.html][3]
  

[4. http://akenzc.com/post/how-to-build-a-blog-with-pelican] [4]
  

[5. https://github.com/getpelican/pelican-plugins/tree/master/better_codeblock_line_numbering][5]
  

[6. http://kevinyap.ca/2013/12/styling-code-blocks-using-pelican/][6]
  

[7. http://whilgeek.github.io/posts/2014/07/we-were-unable-to-load-disqus/][7]


[1]: http://docs.getpelican.com/en/3.5.0/index.html
[2]: https://github.com/DandyDev/pelican-bootstrap3
[3]: http://elfnor.com/pelican-and-markdown-styling-cheat-sheet.html
[4]: http://akenzc.com/post/how-to-build-a-blog-with-pelican
[5]: https://github.com/getpelican/pelican-plugins/tree/master/bet:ter_codeblock_line_numbering
[6]: http://kevinyap.ca/2013/12/styling-code-blocks-using-pelican/
[7]: http://whilgeek.github.io/posts/2014/07/we-were-unable-to-load-disqus/