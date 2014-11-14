# -*- coding: utf-8 -*-
import sys

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zhs'

SITENAME = "jack's Blog"
AUTHOR = 'jacksu'

DISQUS_SITENAME = 'jackblog'
GITHUB_URL = 'https://github.com/jacksu'
#SITEURL = '<http://jacksu.github.com>'
GOOGLE_ANALYTICS = 'UA-53239362-1'
TAG_FEED_ATOM  = 'feeds/%s.atom.xml'
TAG_CLOUD_STEPS = 4
FEED_RSS = 'feeds/all.rss.xml'
DEFAULT_PAGINATION = 10

DEFAULT_CATEGORY ='BigData'
OUTPUT_PATH = '.'
#~ RELATIVE_PATH='true'
RELATIVE_URLS=1
STATIC_PATHS = ["static", ]
PATH = 'posts'
#THEME='./pelican-themes/bs6'

#~ REVERSE_ARCHIVE_ORDER=0

LINKS = (('dofine', 'http://log.dofine.me/'),
		('cnblog',"http://www.cnblogs.com/jacksu-tencent/")
		)

SOCIAL = (
		('github', 'https://github.com/jacksu'),
		)

#GOOGLE_CUSTOM_SEARCH_SIDEBAR = "010017366155264590731:njcqykcxuly"#终于被google收录了!~          
#把各种网页小工具(比如倒计时, 微博展示......)的html代码放在这里 不过要使用farseerfc同学制作的bootsrtap2主题(太赞啦!!)
SIDEBAR_CUSTOM=ur"""
<br>
<Script Language="JavaScript"> 
var timedate= new Date("June 22,2013"); 
var now = new ate(); 
var date = now.getTime() - timedate.getTime(); 
var time = Math.floor(date / (1000 * 60 * 60 * 24)); 
if (time >= 0) ;
document.write("<p style='text-align: center'><strong><font style='color:black;font-size:36px;'>"+time +"</font></strong> days<br/><strong>since GRADUATION from<br/> Shanghai Jiao Tong University</strong></p>");
</Script>

<br>
<a href="http://www.ubuntu.com/"><img src="http://www.ubuntu.com/countdown/banner1.png" border="0" width="180" height="150" alt="The next version of Ubuntu is coming soon"></a><br/>

<br>
<a href="http://read.douban.com/ebook/4460022/?referral_code=9ztqcla6"><img border="0" alt="大集市与教堂" src="http://img3.douban.com/view/ark_article_cover/retina/public/4460022.jpg?v=1403842265.0/"/></a><br>

<br>
<li class="widget-container widget_text">
<h3 class="widget-title">About me</h3>
<div class="textwidget">
毕业于西安电子科技大学，现在就职于tencent，关注大数据技术。<br/>
</div></li>

<br>
<li class="widget-container widget_text">
<h3 class="widget-title">推荐文章</h3>
<div class="textwidget">
<a href="http://x-wei.github.com/google_youku_host_20120706.html">[更新]访问google服务和优酷去广告功能的host列表</a><br>
<a href="https://jacksu.github.io/my-github-blog-set.html">用pelican在github上创建自己的博客!</a><br>
<a href="https://jacksu.github.io/i-love-you.html">我们的故事</a><br>
</div></li>

<br>
<li class="widget-container widget_text">
<h3 class="widget-title">Who are Visiting</h3>
<div class="textwidget">
<script type="text/javascript" src="http://jf.revolvermaps.com/2/1.js?i=59olkba9w7e&amp;s=220&amp;m=3&amp;v=false&amp;r=false&amp;b=000000&amp;n=false&amp;c=ff0000" async="async"></script>
</div></li>

<br>
<!-- UJian Button BEGIN -->
<script type="text/javascript" src="http://v1.ujian.cc/code/ujian.js?type=slide&fade=1"></script>
<a href="http://www.ujian.cc" style="border:0;"><img src="http://img.ujian.cc/pixel.png" alt="友荐云推荐" style="border:0;padding:0;margin:0;" /></a>
<!-- UJian Button END -->
"""

#~ <br>
#~ <object type="application/x-shockwave-flash" style="outline:none;" data="http://hosting.gmodules.com/ig/gadgets/file/112581010116074801021/hamster.swf?" width="300" height="225"><param name="movie" value="http://hosting.gmodules.com/ig/gadgets/file/112581010116074801021/hamster.swf?"></param><param name="AllowScriptAccess" value="always"></param><param name="wmode" value="opaque"></param></object>
#~ <br>

#gtalk
#<iframe src="http://www.google.com/talk/service/badge/Show?tk=z01q6amlq8n8dcqb7mphiivq299uh917bh2sph4lo7rip701jaltqve59eica9opvmhfq5h7hm6i7jkdql1kqntt3h8mnto6ns9lt5960d4dhrvdo3963kv040g9344v6q2nslh6sgqnjp5l2oqspe7p29858omr5qthnm8lc&amp;w=200&amp;h=60" frameborder="0" allowtransparency="true" width="200" height="60"></iframe>
#~ TWITTER_USERNAME = 'farseerfc'

#~ PDF_GENERATOR = True
