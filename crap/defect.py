from crap.commands import BaseShowCommand, BaseListCommand
from crap import utils

class Show(BaseShowCommand):
    "Show details about a single defect"

    def __init__(self, app, app_args):
        super(Show, self).__init__(app, app_args, artifact_type='Defect')


class List(BaseListCommand):
    "Get a list of defects"

    def __init__(self, app, app_args):
        super(List, self).__init__(app, app_args, artifact_type='Defect')


    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        parser.add_argument(
            '-s', '--state',
            nargs='?',
            const='Open',
            default='Open',
            help='The state of the defects to list ([Open], Fixed, Submitted'
            ' Closed, \'In Gating\', All'
            )
        return parser


    def take_action(self, parsed_args):
        state = parsed_args.state.lower()

        # has to be assigned here since it is not available at the time the
        # parent class is constructed

        # validate passed in state argument
        if state.lower() not in ['open', 'closed', 'fixed', 'submitted',
                'in gating', 'all']:
            self.log.info('unknown state: %s' % state)
            raise RuntimeError()

        if state.lower() != 'all':
            self.query = '(State = %s)' % state.title()

        super(List, self).take_action(parsed_args)

        # self.artifacts from the superclass contains the results of our query
        # now we have an object containing the search results, we need to
        # get the good stuff out
        data = [(artifact.FormattedID, utils.strip_html(artifact.Name),
            artifact.State, artifact.ScheduleState) for artifact in self.artifacts]

        columns = ['ID', 'Name', 'State', 'ScheduleState']

        return (columns, data)
