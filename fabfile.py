#!/usr/bin/env python
# init_py_dont_write_bytecode

# init_boilerplate

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.project import *

CWD = os.path.dirname(__file__)
PROJ_HOME = CWD


@task
def self_test():
    '''for use with entr

    find . -name "*.py" |entr fab self_test

    '''
    with lcd(CWD):
        local('pipenv run pytest   -v {}/test -m wip --fulltrace'.format(CWD))


@task
def mon_and_test():
    with lcd(CWD):
        local('ack -f --python | entr fab self_test')
