from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

def test():
	local("nosetests -v")
def commit():
	message = input("Enter a git commit message: ")
	local("git add -A && git commit -m '{0}'".format(message))
def push():
	local("git push origin master")

def prepare():
	test()
	commit()
	push()
