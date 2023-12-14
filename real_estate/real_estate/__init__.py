from . import models
from . import wizard
from . import controller

def _pre_init_hook(cr):
    print('/n/n/n/n/=>I am install')

def _post_init_hook(cr, registry):
    print('/n/n/n/n/=>I am unistall')


def uninstall_hook(cr, registry):
    print('/n//n/n/n/n => i am unistall viren')
       