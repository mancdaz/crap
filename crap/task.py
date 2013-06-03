from crap.commands import BaseShowCommand, BaseListCommand

class Show(BaseShowCommand):
    "Show details about a task"

    def __init__(self, app, app_args):
        super(Show, self).__init__(app, app_args, artifact_type='Task')

class List(BaseListCommand):
    "Show details about a task"

    def __init__(self, app, app_args):
        super(List, self).__init__(app, app_args, artifact_type='Task')
