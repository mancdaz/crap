from crap.commands import BaseShowCommand
from crap.commands import BaseListCommand
from crap import utils

class Show(BaseShowCommand):
    ''' Show details about a single story '''

    def __init__(self, app, app_args):
        super(Show, self).__init__(app, app_args, artifact_type='Story')

class List(BaseListCommand):
    ''' Get a list of stories '''

    def __init__(self, app, app_args):
        super(List, self).__init__(app, app_args, artifact_type='Story')


    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        parser.add_argument(
            '-s', '--state',
            nargs='?',
            const='open',
            default='open',
            help='The state of the artifacts to list (Defined, In-Progress,'
            ' Completed, Accepted, Waiting for Gate). \nMeta state \'open\''
            ' will search for stories in either \'defined\' OR \'in-progress\''
            ' states. \nMeta state \'closed\' will do the opposite'
            )
        return parser


    def take_action(self, parsed_args):

        super(List, self).take_action(parsed_args)

        # has to be assigned here since it is not available at the time the
        # parent class is constructed
        state = parsed_args.state.lower()

        # validate passed in state argument
        if state.lower() not in ['open', 'closed', 'defined', 'in-progress',
                'waiting for gate', 'completed', 'accepted', 'all']:
            self.log.info('unknown state: %s' % state)
            raise RuntimeError()

        # build query
        if state == 'open':
            self.query = '((ScheduleState = Defined) OR '\
            '(ScheduleState = In-Progress))'
        elif state == 'closed':
            self.query = '((ScheduleState != Defined) AND '\
            '(ScheduleState != In-Progress))'
        else:
            self.query = '(ScheduleState = %s)' % state.title()

        # self.artifacts from parent class contains search results

        # now we have an object containing the search results, we need to
        # get the good stuff out
        data = [(artifact.FormattedID, utils.strip_html(artifact.Name),
            artifact.ScheduleState) for artifact in self.artifacts]

        columns = ['ID', 'Name', 'ScheduleState']

        return (columns, data)
