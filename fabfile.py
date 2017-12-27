from fabric.api import local, settings, abort
from fabric.contrib.console import confirm


def test():
	with settings(warn_only=True):
		result = local("nosetests -v", capture=True)
	if result.failed and not confirm("Tests failed, Continue?"):
		abort("aborted at user request.")

def commit():
	message = input("Enter a git commit message: ")
	local("git add -A && git commit -m '{0}'".format(message))
def push():
	local("git branch")
	branch = input("which git branch do you want to push to? ")
	local("git push origin {}".format(master))

def prepare():
	test()
	commit()
	push()

def pull():
	local("git pull origin master")

def heroku():
	local("git push heroku master")

def heroku_test():
	local("heroku run nosetests -v")

def deploye():
	#pull()
	test()
	#commit()
	heroku()
	heroku_test()

def rollback():
	local("heroku rollback")
