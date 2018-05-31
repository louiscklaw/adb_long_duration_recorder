call

find . -name "*.py" |entr pytest -v



# References
### ubuntu
    apt install _swig_

### to install python-usb from source(google)
    cd python-adb
    pipenv shell --three
    pipenv shell
    python //should be something like 3.x.x
    python setup.py install

### start develop
    ack -f --python | entr pipenv run pytest -v ./test -m wip


### command tried seems ok
adb shell "echo \$\$; sleep 999"
will return a pid of that shell

adb kill <pid_of_that_shell>
