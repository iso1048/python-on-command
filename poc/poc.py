
from helpers import *
from commands import *

def main():

    # set up and parse command line arguments
    parser = set_args()
    cl_args = parser.parse_args()

    # retrieve the controls for the command
    command = cl_args.invoked_command
    CC = get_command_controls(command)

    # check that arguments for the invoked command are valid
    check_arguments(command, CC, cl_args)

    # execute the command
    CC['execute'](cl_args)

    return
