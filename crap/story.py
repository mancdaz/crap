import sys

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

        state = parsed_args.state.lower()
        limit = parsed_args.limit

        if limit == 'all':
            limit=None
        else:
            try:
                limit = int(parsed_args.limit)
            except:
                self.log.warning('limit must be a number')
                sys.exit(1)

        # get the rally connection object (note this gets initialised in the
        # initialize_app call in the main App class (Crap)
        rally = self.app.rally
        query = None

        # validate passed in state argument
        if state.lower() not in ['open', 'closed', 'defined', 'in-progress',
                'waiting for gate', 'completed', 'accepted']:
            self.log.debug('unknown state: %s' % state)

        # build query
        if state == 'open':
            query = '((ScheduleState = Defined) OR (ScheduleState = In-Progress))'
        elif state == 'closed':
            query = '((ScheduleState != Defined) AND (ScheduleState != In-Progress))'
        else:
            query = '(ScheduleState = %s)' % state.title()


        self.log.debug('using query: %s' % query)
        self.log.debug('showing first %s results' % limit) 

        # do the search
        artifacts = utils.do_rally_query(rally, self.artifact_type, query=query, limit=limit)

        # now we have an object containing the search results, we need to
        # get the good stuff out
        data = [(artifact.FormattedID, utils.strip_html(artifact.Name), artifact.ScheduleState) for artifact in artifacts]

        columns = ['ID', 'Name', 'ScheduleState']

        return (columns, data)
