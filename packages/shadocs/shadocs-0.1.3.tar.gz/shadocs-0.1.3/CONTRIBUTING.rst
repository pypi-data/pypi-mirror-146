.. highlight:: shell

============
贡献
============

欢迎提交你的贡献。

你可以通过多种方式进行贡献:

贡献类型
----------------------

提交 Bugs 
~~~~~~~~~~~

可以在 https://github.com/llango/shadocs/issues 提交 bug 。

当你提交 bug，建议你说明一下几点：

* 你的操作系统机器版本。
* 对故障排除有帮助的任何详细信息。
* 重现 bug 的详细步骤。

修复 Bugs 
~~~~~~~~

查看Github issues 任何有关 bug 信息，然后进行修复提交。

实现功能
~~~~~~~~~~~~~~~~~~

查看Github issues 任何有关功能实现的信息。 标有 "enhancement" 和 "help wanted" 是对想要实现这功能开放。

编写文档 
~~~~~~~~~~~~~~~~~~~

欢迎丰富 Shadocs 文档 。


提交反馈
~~~~~~~~~~~~~~~

最好提交反馈的方式在： https://github.com/llango/shadocs/issues.

如果你想提出一个功能:

* 详细解释它是如何工作的。
* 尽量缩小范围，使其更容易实现。
* 请记住，这是一个由志愿者驱动的项目，欢迎你的贡献:)

开始
------------

做好准备贡献了吗? 
这里是安装 `shadocs` 进行本地开发的。

1. 从 Github `shadocs` 克隆到本地：

    $ git clone git@github.com:your_name_here/shadocs.git

2. 将您的本地副本安装到你的Python 虚拟环境中。假设您已经安装了virtualenvwrapper，你可以如下方式操作::

    $ mkvirtualenv shadocs
    $ cd shadocs/
    $ python setup.py develop

3. 给本地开发创建一个分支::

    $ git checkout -b name-of-your-bugfix-or-feature

   现在你可以本地修改你的代码了。

4. 当你完成了开发，检查你的修改是否通过了 flake8 和 测试，包括使用 tox 测试其他 Python 版本::

    $ flake8 shadocs tests
    $ python setup.py test or pytest
    $ tox

   获取 flake8 和 tox 的方式：直接 pip install 安装便可。

5. 提交你的修改并将你的分支推到GitHub上::

    $ git add .
    $ git commit -m "关于你的修改详细信息。"
    $ git push origin name-of-your-bugfix-or-feature

6. 通过GitHub网站提交pull请求。

Pull 请求操作
-----------------------

在你提交 pull 请求之前，检查它是否符合这些条件:

1. pull 请求应该包括测试。
2. 如果 pull 请求增加了功能，则应该更新文档。把将新功能添加到带有 docstring 的函数中，并且将该功能添加到 README.rst 的列表中。
3. pull 的功能应该满足Python 3.5, 3.6, 3.7 and 3.8, and for PyPy. 检查
   https://travis-ci.com/llango/shadocs/pull_requests
   并确保测试通过了所有支持的Python版本。

提示
----

运行测试的子集::::


    $ python -m unittest tests.test_shadocs

发布
---------

针对维护人员如何部署进行提示:
确保提交了所有的更改(包括在 HISTORY.rst 中的添加项)。
然后运行::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags

然后，如果测试通过，Travis将部署到PyPI。
