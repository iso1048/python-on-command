
import os
import sys
import argparse
from commands import *

def check_filepath(filepath, required_filetype=None):
    """
    Checks that <filepath> is 1) a valid path, and 2) of the required    \
    filetype. An invalid filepath raises a FileNotFoundError, and valid  \
    filepaths whose extension are not of <required_filetype> raise an    \
    ArgumentError. 

    @param  filepaths : str
        path to the file
    @param  required_filetype : str
        file type without the preceeding '.' i.e. 'pdf', not '.pdf'. 
        Defaults to None.
    
    @return True (or raises a FileNotFoundError or ArgumentError)
    """

    filename, file_extension = os.path.splitext(filepath)
    if required_filetype:
        required_filetype_lc = required_filetype.lower()

    if not os.path.isfile(filepath):
        raise FileNotFoundError('{} is not a valid filepath'.format(filepath))
    elif required_filetype and '.'+required_filetype_lc != file_extension:
        error_msg = '{} is not the expected filetype ({})'.format(filepath, required_filetype)
        raise argparse.ArgumentTypeError(error_msg) 
    else:
        return True

def check_page_format(page_input):
    """
    Checks that page_input is in the correct format - either a single,    \
    non-zero page number or a page range in the format X-Y (where X < Y). 

    @param  page_input : str
        Page number or page range input by the user at the command line

    @return True (or raises ValueError for invalid page input)
    """
    error_msg = 'Invalid argument. {} is not a valid page/page range'.format(page_input)

    try:
        # test if page_input is a page range
        if '-' in page_input:
            page_range_split = page_input.split('-')

            if len(page_range_split) == 2:
                start, end = int(page_range_split[0]), int(page_range_split[1])
                if start < end:
                    return True

        # test if page_input is a single page number
        elif int(page_input) > 0:
            return True
 
        raise ValueError

    except ValueError:
        raise ValueError(error_msg)

def set_args():
    """
    Set up parser for command line arguments. Creates subparsers to allow
    different commands to be run from the command line.

    @return parser : ArgumentParser
    """
    parser = argparse.ArgumentParser()

    # initialise subparsers to handle different functionality
    subparsers = parser.add_subparsers(help='command help', dest='invoked_command', required=True)

    # subparser for 'merge' command
    parser_merge = subparsers.add_parser('merge', 
        help='merges two or more pdf files into a single pdf file')
    parser_merge.add_argument('pdfs', 
        help='paths to two or more pdf files',
        nargs='+')

    # subparser for 'remove' command
    parser_remove = subparsers.add_parser('remove',
        help='remove pages from a pdf file')
    parser_remove.add_argument('src_pdf',
        help='path to the pdf file to remove pages from')
    parser_remove.add_argument('pages',
        help='pages to remove from the source pdf, given as page number/s\
            and/or page range/s in the format X-Y (inclusive) where X and\
            Y are non-zero and X < Y e.g. \'2-3 5-7 9\' would remove \
            pages 2, 3, 5, 6, 7, and 9 from the source pdf.',
        nargs='+')

    # subparser for 'insert' command
    parser_insert = subparsers.add_parser('insert',
        help='insert one pdf file into another pdf file, after the given \
            page number')
    parser_insert.add_argument('src_pdf',
        help='path to the source pdf file into which <ins_pdf> will be \
            inserted')
    parser_insert.add_argument('ins_pdf',
        help='path to the pdf file to insert into <src_pdf>')
    parser_insert.add_argument('page',
        help='page number in <src_pdf> which <ins_pdf> will be inserted \
            after e.g. if <page> is 5, then <ins_pdf> will be inserted \
            after page 5 of <src_pdf>, such that the first page of \
            <ins_pdf> will be page 6 in the output pdf file',
        type=int)
    
    # subparser for 'split' command
    parser_split = subparsers.add_parser('split',
        help='split a pdf file into separate pdf files')
    parser_split.add_argument('src_pdf',
        help='path to the source pdf file which is to be split')
    parser_split.add_argument('pages',
        help='pages to save as separate pdf files, given as single page \
            numbers or a range of pages in the format X-Y (inclusive) \
            where X and Y are non-zero and X < Y e.g. \'2-3 5-7 9\' would\
            save pages 2-3, 5-7, and 9 in the source pdf as three separate\
            pdf files.', 
        nargs='+')

    # more to come ...
    # convert

    # print(parser.parse_args(['merge', 'path1', 'path2', 'path3']))

    return parser

def get_command_controls(command):
    """
    Maps a command to 

    @param  command : str
        Command input by the user. E.g. merge, remove. 
        
    @return cc[command] : dict
        dict containing the following properties for the given command: 
        arg_name, arg_checks, min_args, 
    """

    cc = {
        'merge':{
            'arg_name': ['pdfs'],
            'arg_checks': [lambda path: check_filepath(path, 'pdf')],
            'min_args': 2,
            'execute': merge
        },
        'remove': {
            'arg_name': ['src_pdf', 'pages'],
            'arg_checks': [check_filepath, check_page_format],
            'min_args': 2,
            'execute': remove
        },
        'insert': {
            'arg_name': ['src_pdf', 'ins_pdf', 'page'],
            'arg_checks': [check_filepath, check_filepath, lambda x: True],
            'min_args': 3,
            'execute': insert
        },
        'split': {
            'arg_name': ['src_pdf', 'pages'],
            'arg_checks': [check_filepath, check_page_format],
            'min_args': 2,
            'execute': split 
        }
    }

    return cc[command]

def check_arguments(command, command_control, cl_arguments):
    """
    Checks that all arguments given at the command line are valid. 

    @param  command : str
        Command input by the user. E.g. merge, remove.

    @param  command_control : dict
        Dict mapping a command to its argument names, argument checking
        functions, and the function to execute the required behaviour.

    @param  cl_arguments : argparse.Namespace
        Parsed arguments returned from calling ArgumentParser.parse_args().
    
    @return None (or raises an exception)

    """

    # ensure correct number of arguments were given
    if len(sys.argv[2:]) < command_control['min_args']:
        raise Exception('{} expects at least {} arguments'.format(command, command_control['min_args']))

    # ensure that the given arguments are valid
    for arg_name, check_func in zip(command_control['arg_name'], command_control['arg_checks']):
        arguments = getattr(cl_arguments, arg_name)
        if arguments:
            if isinstance(arguments, list):
                for arg in arguments:
                    check_func(arg)
            else:
                check_func(arguments)

    return None



