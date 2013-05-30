from crap.commands import BaseShowCommand
from crap.commands import BaseListCommand

class Show(BaseShowCommand):
    ''' Show details about a single story '''

    def __init__(self, app, app_args):
        super(Show, self).__init__(app, app_args, artifact_type='Story')

class List(BaseListCommand):
    ''' Get a list of all stories '''

    def __init__(self, app, app_args):
        super(List, self).__init__(app, app_args, artifact_type='Story')
