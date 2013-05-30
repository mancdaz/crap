from crap.commands import BaseShowCommand

class Show(BaseShowCommand):
    "Show details about a defect"

    def __init__(self, app, app_args):
        super(Show, self).__init__(app, app_args, artifact_type='Defect')
