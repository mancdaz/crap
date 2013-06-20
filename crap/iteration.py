from datetime import datetime
from cliff.lister import Lister
import logging
import re
#from crap import utils

class Show(Lister):
    ''' Show all stories/tasks/defects in an iteration '''

    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(Show, self).__init__(app, app_args)

    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)
        parser.add_argument(
                dest='iteration', nargs='?', type=int)
        return parser

    def take_action(self, parsed_args):

        iteration = parsed_args.iteration
        rally = self.app.rally

        # if we were just passed a number, try and make it into something
        # more like an iteration name, that we can use
        if re.match(r'\d+', str(iteration)):
            iteration = 'Iteration %s' % iteration

        self.log.info(iteration)

        # find the name of the current iteration if no iteration number
        # was provided
        if not iteration:
            now = datetime.now().isoformat()
            query = '((EndDate >= %s) and (StartDate <= %s))' % (now, now)
            self.log.info(query)
            try:
                i = rally.get('Iteration', query=query, instance=True, fetch='Name')
                iteration = i.Name
            except:
                raise RuntimeError('could not get info about current iteration. '
                        ' Be sure there is currently an active iteration')


        columns = ['Name']
        data = [[iteration]]

        return (columns, data)
