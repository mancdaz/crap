import logging
import sys
import os
#from pyral import Rally

from cliff.app import App
from cliff.commandmanager import CommandManager
from crap import utils


VERSION = '0.1'

def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.

    """

    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


class Crap(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(Crap, self).__init__(
                description='crap rally cli',
                version='VERSION',
                command_manager=CommandManager('cliff.crap'),
                )


        def build_option_parser(self, description, version):
            parser = super(Crap, self).build_option_parser(
                    description,
                    version,
                    {"conflict_handler": 'resolve'})

            # Global arguments
            parser.add_argument(
                '-d', '--debug',
                action='store_true',
                default=False,
                dest='debug',
                help='enable debug output')
            parser.add_argument(
                '--rally-server',
                default=env('RALLY_SERVER'),
                dest='rally_server',
                help='url of the rally server (env: RALLY_SERVER)')
            parser.add_argument(
                '--rally-username',
                default=env('RALLY_USERNAME'),
                dest='rally_username',
                help='rally username (env: RALLY_USERNAME)')
            parser.add_argument(
                '--rally-password',
                default=env('RALLY_PASSWORD'),
                dest='rally_password',
                help='rally password (env: RALLY_PASSWORD')
            parser.add_argument(
                '--rally-project',
                default=env('RALLY_PROJECT'),
                dest='rally_project',
                help='rally project (env: RALLY_PROJECT)')

            return parser


    def initialize_app(self, argv):
        self.log.debug('initialize_app')

        requests_log = logging.getLogger("requests")
        if self.options.debug:
            requests_log.setLevel(logging.DEBUG)
        else:
            requests_log.setLevel(logging.WARNING)

        # get the rally connection object that will be used by all subcommands
        self.rally = utils.get_rally_connection(
                self.options.rally_username,
                self.options.rally_password,
                self.options.rally_project,
                self.options.rally_server)



        def prepare_to_run_command(self, cmd):
            self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = Crap()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
