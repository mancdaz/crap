from crap.commands import BaseShowCommand
from crap.commands import BaseListCommand
from crap import utils

class Show(BaseShowCommand):
    ''' Show details about a single story '''

    def __init__(self, app, app_args):
        super(Show, self).__init__(app, app_args, artifact_type='Story')

class List(BaseListCommand):
    ''' Get a list of all stories '''

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
        # can use directly from the parent class since it is parsed there
        limit = self.limit

        # get the rally connection object (note this gets initialised in the
        # initialize_app call in the main App class (Crap)
        rally = self.app.rally

        # validate passed in state argument
        if state.lower() not in ['open', 'closed', 'defined', 'in-progress',
                'waiting for gate', 'completed', 'accepted']:
            self.log.info('unknown state: %s' % state)
            raise RuntimeError()

        # build query
        query = None
        if state == 'open':
            query = '((ScheduleState = Defined) OR '\
            '(ScheduleState = In-Progress))'
        elif state == 'closed':
            query = '((ScheduleState != Defined) AND '\
            '(ScheduleState != In-Progress))'
        else:
            query = '(ScheduleState = %s)' % state.title()

        # some debug output
        self.log.debug('using query: %s' % query)
        if limit: self.log.debug('showing first %s results' % limit)

        # do the search
        artifacts = utils.do_rally_query(
            rally, self.artifact_type, query=query, limit=limit, fetch=True)

        # now we have an object containing the search results, we need to
        # get the good stuff out
        data = [(artifact.FormattedID, utils.strip_html(artifact.Name),
            artifact.ScheduleState) for artifact in artifacts]

        columns = ['ID', 'Name', 'ScheduleState']

        return (columns, data)
