Title: 个人github blog环境设置
Date: 2014-7-27 00:20
Modified: 2014-7-27 00:20
Category: env_set
Tags: github
Slug: my-github-blog-set
Author: jacksu
Summary: 每个人都想拥有自己的网站，但是大部分比较屌丝，不想花钱租赁服务器，哈哈，屌丝有屌丝办法。github应该都听说过吧，github.io提供了此功能，而且使用github来管理自己的代码，如果你有域名，还可以绑定你自己的域名欧。我在github的博客终于捣鼓好了，也给大家介绍一下建站步骤。

#软件安装

大体需要以下几个东东，个性化的就需要自己去搜寻。
##pelican
###安装
我们需要网站的管理工具pelican，pelican可以把markdown的文件生成html和pdf，pelican又依赖于pipe，安装命令如下：<br>
`sudo easy_install pipe`<br>
`sudo pip install pelican`<br>
###检查是否安装成功
执行如下命令：<br>
`pelican -h`或者
`pelican .md所在目录`
##Markdown包
pelican不可以识别markdown，需要下载markdown包，markdown的下载方式为：<br>
`sudo pip install Markdown`
##主题
没有主题，你的网站太难看了，那么下载一个主题：
`git clone https://github.com/farseerfc/pelican-themes`
#设置
##github上的设置
在github上建立**`username.github.io`**的项目（如何在github建立项目，我就不说了，应该很多人会），参考[官方文档](https://help.github.com/articles/creating-pages-with-the-automatic-generator)设置，过**十分钟**左右你就可以通过`username.github.io`访问了。
##settings.py设置
settings.py的内容大体如下，我也是参考[mx的blog](http://x-wei.github.io/pelican_github_blog.html)的.

	# -*- coding: utf-8 -*-
	import sys

	TIMEZONE = 'Asia/Shanghai'

	DEFAULT_LANG = 'zhs'

	SITENAME = "X. Wei's Blog"
	AUTHOR = 'X.Wei'

	DISQUS_SITENAME = 'xweisblog'
	GITHUB_URL = '<https://github.com/X-Wei>'#github链接
	SITEURL = '<http://x-wei.github.com>'
	GOOGLE_ANALYTICS = 'UA-30756331-1'#谷歌站点分析
	TAG_FEED  = 'feeds/%s.atom.xml'

	DEFAULT_PAGINATION = 4#默认每一页有多少篇文章

	DEFAULT_CATEGORY ='misc'
	OUTPUT_PATH = '.'
	#需要把输出路径从默认的'output'改成根目录(your_id.github.com目录), 因为githubpage需要把index.html上传到repo的master分支的根目录才可以!
	PATH = 'posts'#这个是指定放置.md/.rst文件的目录

	LINKS = (('dofine', '<http://www.dofine.me>'),
    	     ('farseerfc', "<http://farseerfc.github.com/>"),
     	    )#友情链接~

	SOCIAL = (
	          ('github', '<https://github.com/x-wei>'),
    	      )#社交网络链接
        	  #~ ('twitter', '<http://twitter.com/farseerfc>'),
	          #~ ('facebook', '<http://www.facebook.com/farseerfc>'),
	          #~ ('weibo', '<http://weibo.com/farseerfc>'),
	          #~ ('renren', '<http://www.renren.com/farseer>'),

	#这个是farseerfc同学自己加的, 可以显示他的新浪微博内容, 有微博的话可以把这些加上~
	#~ TWITTER_USERNAME = 'farseerfc'
	#~ SIDEBAR_CUSTOM = r"""
	#~ <li class="nav-header"><h4><i class="icon-list-alt"></i>Weibo</h4></li>
	#~ <iframe width="100%" height="550" class="share_self"  frameborder="0" scrolling="no" 
	#~ src="<http://widget.weibo.com/weiboshow/index.php?language=&width=0&height=550&fansRow=1&ptype=1&speed=0&skin=2&isTitle=1&noborder=1&isWeibo=1&isFans=1&uid=1862842353&verifier=b193b9de&dpc=1>">
	#~ </iframe>
	#~ """

	#google自定义搜索(大概是站内搜索吧)
	#~ GOOGLE_CUSTOM_SEARCH_SIDEBAR = "001578481551708017171:axpo6yvtdyg"
	#~ GOOGLE_CUSTOM_SEARCH_NAVBAR = "001578481551708017171:hxkva69brmg"

我的[settings.py](https://github.com/jacksu/jacksu.github.io/blob/master/settings.py)。

#建站
把刚才github的项目拉到本地，执行如下命令：

`git clone https://github.com/username/username.github.io`<br>
`pelican -s settings.py -t ../pelican-themes/bootstrap2/ posts/`

其中－t后面是你的主题目录，posts是md所在的目录。再执行如下命令:

`git add .`

`git commit -m "add"`

`git push`

我们的个人网站建成了，可以访问`usrname.github.io`了。