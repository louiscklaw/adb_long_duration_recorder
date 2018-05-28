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
