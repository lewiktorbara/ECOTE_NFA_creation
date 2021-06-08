
from optparse import OptionParser
import sys

from Errors.log import Log
from Errors.error_library import ErrorLibrary, get_error_lib
from StringComparison.comparator import  comparison

error_lib = get_error_lib()
logs = []

if __name__ == "__main__":
    
    # CLI Parsing
    usage = "usage: %prog [options] regural_expression_file strings_file [output_file]"
    opt_parser = OptionParser(usage=usage)

    opt_parser.add_option("-s", "--silent", action="store_true", dest="silent", default=False, help="turns off the error/warning output")
    opt_parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="generates descriptive error/warning messages")
    opt_parser.add_option("-n", "--nowarn", action="store_false", dest="warnings", default=True, help="mutes warning output")
    opt_parser.add_option("-o", "--output", action="store", type="string", dest="filename", help="redirects the error/warning output to a file")

    (options, args) = opt_parser.parse_args()

    # CLI Errors/Warnings
    if options.silent and options.verbose:
        opt_parser.error("Options -s and -v are mutually exclusive.")
    if len(args) < 2:
        opt_parser.error("Too few input file provided!")    
    if len(args) > 3:
        print("More thatn 3 arguments provided, excess arguments will be ignored.")
    
    # Assigning I/O variables
    if options.filename == None:
        log_out = sys.stdout
    else:
        log_out = open(options.filename, 'w')

    re_file = args[0]
    strings_file = args[1]
    if len(args) == 2:
        output_file = "output"
    else:
        output_file = args[2]
    
    if re_file == output_file or strings_file == output_file:
        if not options.silent and options.warnings:
            warn = error_lib.get_error("w80")
            if options.verbose:
                warn_str = warn.what_long(None, [output_file])
            else:
                warn_str = warn.what_short(None)
            print(warn_str, file = log_out)
    
    # Get the input
    try:
        with open(re_file, 'r') as file:
            re = file.readline()
        with open(strings_file, 'r') as file:
            strings = file.readlines()
    except FileNotFoundError as e:
        if not options.silent:
            er = error_lib.get_error("e98")
            if options.verbose:
                er_str = er.what_long(None, [e.strerror])
            else:
                er_str = er.what_short(None)
            print(er_str, file=log_out)
        exit()


    # Calling creation and comparison of nfa and strings
    try:
        outpt = comparison(re, strings, logs)[1]
    except Log as e:
        if not options.silent:
            print("Execution unsuccesful.", file=log_out)
            if options.verbose:
                er_str = error_lib.what_long(e)
            else:
                er_str = error_lib.what_short(e)
            print(er_str, file=log_out)
        exit()

    # Print warnings
    if not options.silent and options.warnings:
        if len(logs) == 1:
            print("Execution completed with %d warning:" % len(logs), file=log_out)
        elif len(logs) > 1:
            print("Execution completed with %d warnings:" % len(logs), file=log_out)
        else:
            print("Execution completed with no warnings.", file=log_out)
        for log in logs:
            if options.verbose:
                warn_str = error_lib.what_long(log)
            else:
                warn_str = error_lib.what_short(log)
            print(warn_str, file=log_out)


    # Output
    try:
        with open(output_file, 'w') as file:
            file.writelines(outpt)
            
    except FileNotFoundError as e:
        if not options.silent:
            er = error_lib.get_error("e98")
            if options.verbose:
                er_str = er.what_long(None, [e.strerror])
            else:
                er_str = er.what_short(None)
        print(er_str, file=log_out)
        exit()
    





    #logs = []
    #strings = ['110ax', '1']
    #print(comparison('1*.(0|a)*.x', strings, logs))
    #print(conversion('1*.(0|a).x', logs))
    #print(logs[0].err_code)
    '''
    # Print warnings
    if len(logs) == 1:
        print("Execution completed with %d warning:" % len(logs))
    elif len(logs) > 1:
        print("Execution completed with %d warnings:" % len(logs))
    else:
        print("Execution completed with no warnings.")
    for log in logs:
        warn_str = error_lib.what_long(log)
        print(warn_str)
    '''