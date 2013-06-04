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
        query = 'FormattedID = %s' % FormattedID
        artifact_obj = utils.do_rally_query(rally, self.artifact_type, query=query, fetch=True)

        # did we get a valid artifact? If no name, assume not
        try:
            name = utils.strip_html(str(artifact_obj.Name))
        except AttributeError:
            self.log.error("Could not find %s : %s" % (self.artifact_type, FormattedID))
            sys.exit(1)

        # quickly and dirtily remove html elements if present
        desc = utils.strip_html(str(artifact_obj.Description))

        # get associated tasks by FormattedID and Name
        try:
            tasks = '\n'.join(['%-7s: %s' % (s.FormattedID,  utils.strip_html(s.Name)) for s in artifact_obj.Tasks])
        except AttributeError:
            tasks = None

        # Stories don't have 'State' Attribute
        try:
            state = artifact_obj.State
        except AttributeError:
            state = None

        # is this part of an iteration?
        try:
            iteration = getattr(getattr(artifact_obj, 'Iteration'), 'Name')
        except AttributeError:
            iteration = None

        # tasks don't have 'ScheduleState' Attribute
        try:
            schedulestate = artifact_obj.ScheduleState
        except AttributeError:
            schedulestate = None

        # do we have an owner? If so try a few ways to get the name
        try:
            owner = "%s %s" %\
                (artifact_obj.Owner.FirstName, artifact_obj.Owner.LastName)
            if owner == "None None":
                owner = artifact_obj.Owner.DisplayName
            if owner == None:
                owner = artifact_obj.Owner.UserName
        except AttributeError:
            owner = None

        # build the return data
        columns = ['Name', 'ID', 'Iteration',
                'Description', 'ScheduleState', 'State', 'Owner',  'Tasks']
        data = [name, artifact_obj.FormattedID,
                iteration, desc, schedulestate, state, owner, tasks]

        return (columns, data)

class BaseListCommand(Lister):
    ''' The base list command class implemented by defect-list, task-list
    story-list '''

    log = logging.getLogger(__name__)

    def __init__(self, app, app_args, artifact_type):
        super(BaseListCommand, self).__init__(app, app_args)
        self.artifact_type = artifact_type
        self.limit = None

    def get_parser(self, prog_name):

        parser = super(BaseListCommand, self).get_parser(prog_name)
        parser.add_argument(
            '-l', '--limit',
            nargs='?',
            const='20',
            default='20',
            help='Number of results to show (default=20)'
            )
        return parser

    def take_action(self, parsed_args):

        self.limit = parsed_args.limit

        if self.limit == 'all':
            self.limit=None
        else:
            try:
                self.limit = int(parsed_args.limit)
            except:
                self.log.warning('limit must be a number')
                sys.exit(1)
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
