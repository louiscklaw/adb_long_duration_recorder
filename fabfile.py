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

    # TEST_COMMANDS = 'pipenv run pytest   -v {}/test -m wip --fulltrace'.format(CWD)
    TEST_COMMANDS = 'pipenv run pytest -v {}/test --fulltrace'.format(CWD)

    with lcd(CWD):
        local(TEST_COMMANDS)


@task
def mon_and_test():
    with lcd(CWD):
        local('ack -f --python | entr fab self_test')


@task
def helloworld():
    print('helloworld')


@task
@hosts('localhost')
def init_fabric_mon_and_test():
    # local('mkdir -p /tmp/{local,remote}')
    WORK_DIR = ['/tmp/local', '/tmp/remote']
    rsync_project(
        local_dir=WORK_DIR[0], remote_dir=WORK_DIR[1],
        delete=True, extra_opts='-azhWu')
    # -u Do Not Overwrite the Modified Files at the Destination
    local('ack -f --python | entr fab helloworld')
