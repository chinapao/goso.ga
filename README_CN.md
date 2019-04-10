[GOSO.GA](https://www.goso.ga)
=====
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)

注意：GOSO.GA已经加入了反996授权协议。请本项目的使用者遵守使用协议！

[English Version](https://github.com/chinapao/README.md)
---

GOSO.GA是一个基于[Searx](https://github.com/asciimoo/searx)开发的隐私搜索引擎。聚合了Google,Bing,Wiki,等主流搜索引擎，能实现文章、新闻、地图、图片、音乐、文件以及种子等内容的搜索。
---
与Searx相比一些主要的提升：

* 优化了性能
* 搜索引擎网站模板更容易修改和自定义
* 将部分网页静态化
* 提升了搜索引擎的隐私保护

To Do List
---
* 集成包括Baidu，SOSO在内的一些搜索引擎
* 进一步提升性能
* 增强对网络攻击的防护能力


**安装方法**
~~~~~~~~~~~~
CentOS 7
-  安装 pip:
    yum install -y epel-release
    yum install -y python-pip
-  获取项目源码:
   ``git clone https://github.com/chinapao/goso.ga.git && cd searx``
-  一键安装依赖: 
   ``pip install -r requirements.txt``
-  编辑设置文件
   `settings.yml' 你需要自定义其中的Secret Key
-  运行 ``python searx/webapp.py`` 
-  可以使用screen 来守护进程  screen -S goso


