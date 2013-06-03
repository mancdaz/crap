import logging
import sys
import re
import crap.utils as utils

from cliff.show import ShowOne
from cliff.lister import Lister

class BaseShowCommand(ShowOne):
    ''' The base show command class implemented by defect-show, task-show
    story-show '''

    log = logging.getLogger(__name__)

    def __init__(self, app, app_args, artifact_type):
        super(BaseShowCommand, self).__init__(app, app_args)
        self.artifact_type = artifact_type

    def get_parser(self, prog_name):
        parser = super(BaseShowCommand, self).get_parser(prog_name)
        parser.add_argument('artifact', nargs='?')
        return parser

    def take_action(self, parsed_args):

        FormattedID = parsed_args.artifact

        # get the rally connection object (note this gets initialised in the
        # initialize_app call in the main App class (Crap)
        rally = self.app.rally

        # ensure we have a valid FormattedID
        if not re.match(rally.FORMATTED_ID_PATTERN, FormattedID):
            self.log.error('%s is not a valid rally artifact ID' % FormattedID)
            sys.exit(1)

        # get the rally artifact object
        artifact_obj = utils.get_rally_artifact_obj(rally, self.artifact_type, FormattedID)

        # did we get a valid artifact? If no name, assume not
        try:
            name = utils.strip_html(str(artifact_obj.Name))
        except AttributeError:
            self.log.error("Could not find %s : %s" % (self.artifact_type, FormattedID))
            sys.exit(1)

        # quickly and dirtily remove html elements if present
        desc = utils.strip_html(str(artifact_obj.Description))

        # get associated tasks by FormattedID and Name
        tasks = None
        if hasattr(artifact_obj, 'Tasks'):
            tasks = '\n'.join(['%-7s: %s' % (s.FormattedID,  utils.strip_html(s.Name)) for s in artifact_obj.Tasks])

        if self.artifact_type == 'Story':
            state = artifact_obj.ScheduleState
        else:
            state = artifact_obj.State

        # build the return data
        columns = ['Name', 'ID', 'Description', 'State', 'Tasks']
        data = [name, FormattedID, desc, state , tasks]

        return (columns, data)

class BaseListCommand(Lister):
    ''' The base list command class implemented by defect-list, task-list
    story-list '''

    log = logging.getLogger(__name__)

    def __init__(self, app, app_args, artifact_type):
        super(BaseListCommand, self).__init__(app, app_args)
        self.artifact_type = artifact_type

    def get_parser(self, prog_name):

        parser = super(BaseListCommand, self).get_parser(prog_name)
        parser.add_argument(
            '-l', '--limit',
            nargs='?',
            const='Limit',
            default='20',
            help='Number of results to show'
            )
        return parser

#    def take_action(self, parsed_args):
#
#        state = parsed_args.state
#        print state
#
#        # get the rally connection object (note this gets initialised in the
#        # initialize_app call in the main App class (Crap)
#        rally = self.app.rally
#        query = None
#
#        if state.lower() is 'open':
#            query = 'State != Completed'
#        if state.lower() is 'closed':
#            query = 'State != Open'
#
#        # do the search
#        artifacts = utils.do_rally_query(rally, self.artifact_type, query=query)
#
#        # now we have an object containing the search results, we need to
#        # get the good stuff out
#        data = [(artifact.FormattedID, artifact.Name) for artifact in artifacts]
#
#        columns = ['ID', 'Name']
#
#        return (columns, data)
