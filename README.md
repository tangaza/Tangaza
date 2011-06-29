TANGAZA
=======
Thanks for choosing Tangaza. A mobile phone-based group messaging system

System Requirements
-------------------

Tangaza runs on Linux. It has been tested only on Debian based distros.
These requirements show the minimum versions of software that the system
has been tested with and that are required to successfully run.

1. Perl 5
2. Python 2.6
3. MySQL 5.0
4. Django 1.2
5. Kannel 1.4.3
6. Asterisk 1.6.2
7. Common Library (http://github.com/tangaza/Common)

Installation:
---------------

Build the application using git-buildpackage in debian
and then install the debian package. This usually means

git clone https://github.com/tangaza/Tangaza
git checkout -b upstream --track origin/master
(The '--track' option alters your .git/config file and adds a [branch "upstream"] section telling Git where you fetched it from. That means you can later just say "git pull" and you will get both the 'master' and the 'upstream' repository merged into your repository automatically.)
git checkout master
git-buildpackage --git-ignore-new
