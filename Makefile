gui:
	pyuic4 -o NixURL/uipy/ui_mainwindow.py NixURL/ui/main.ui
	pyuic4 -o NixURL/uipy/ui_about.py NixURL/ui/about.ui
	pyrcc4 -o NixURL/uipy/nixurl_rc.py NixURL/ui/nixurl.qrc
	
dist:
	python setup.py sdist --format=bztar
	
pyflakes:
	pyflakes NixURL/*.py

pylint:
	pylint NixURL/*.py

install: 
	python setup.py install

clean:
	rm -f *.py{c,o} */*.py{c,o} */*/*.py{c,o}
	rm -fr build
