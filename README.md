[GOSO.GA](https://www.goso.ga)
=====
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)

Notice: GOSO.GA Project has joined the Anti-996 License program.  User of this project must follow the general rule of the license.

[中文版](https://github.com/chinapao/README_CN.md)
---

GOSO.GA is a Privacy Metasearch Engine, based on [Searx](https://github.com/asciimoo/searx)
---
Compare to Searx, the below parts have been improved:

* Improved performance
* Easy to modify templates
* Static web page files
* Improved Privacy Protection

To Do List
---
* Integration of Chinese Search Engines
* More improvements on performance
* Improvement on protection against attacks


**Installation**
~~~~~~~~~~~~

-  install pip:
    yum install -y epel-release
    yum install -y python-pip
-  clone source:
   ``git clone https://github.com/chinapao/goso.ga.git && cd goso.ga``
-  install dependencies: 
   ``pip install -r requirements.txt``
-  edit your
   `settings.yml' You need to Change the Secret_key for your own one
-  run ``python searx/webapp.py`` to start the application


