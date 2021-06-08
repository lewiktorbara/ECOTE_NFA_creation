# Module handling the library of all existing errors/warnings

from .error import Error
from .log import Log

class ErrorLibException(Exception):
    # Exception for internal errors of the library

    def __init__(self, message: str):
        """
        Args:
            message (str):      the internal error message
        """
        self.message = message

class ErrorLibrary():
    # Class for storing an error library
    """
    Atributes:
        library [Error]:        the list of errors/warnings in the library
    """

    def __init__(self):
        self.library = []

    def get_error(self, code: str) -> Error:
        # Gets the error from the library given an error code
        """
        Can throw ErrorLibExcepyion

        Args:
            code (str):         the code of the error
        """
        for er in self.library:
            if er.code == code:
                return er
        
        return ErrorLibException("Error code not in library")

    def what_short(self, log: Log) -> str:
        # Gets the short description of an error given a Log
        """
        Can throw ErrorLibException

        Args:
            log (Log):          log on basis of which to generate the error message
        """
        return self.get_error(log.err_code).what_short(log.line)

    def what_long(self, log: Log) -> str:
        #Gets the verbose description of an error given a Log
        """
        Can throw ErrorLibException
        Args:
            log (Log):      log on basis of which to generate the error message
        """
        return self.get_error(log.err_code).what_long(log.line, log.args)


def get_error_lib():
    # Gets the error library with the defined errors.

    lib = ErrorLibrary()

    # Errors

    # Conversion Errors
    # e10 args: 0 - name of the special character
    e = Error("e10", "Not defined character in RE")
    e.verbose = lambda args: "The regular expression contains character: \'" + args[0] + "\', that is not number or a letter or one of the special symbols { '(' , ')' , '?' , '+' , '*' , '.' , '|' }."
    lib.library.append(e)

    # e11
    e = Error("e11", "Lack of left parenthesis")
    e.verbose = lambda args: "The regular expression reader encountered ‘)’ while there was not corresponding symbol ‘(‘ before"
    lib.library.append(e)

    # e12
    e = Error("e12", "Lack of right parenthesis")
    e.verbose = lambda args: "The regular expression reader encountered ‘(‘ that was not closed by the ‘)’ symbol"
    lib.library.append(e)

    # e13 args: 0 - symbol that was encountered
    e = Error("e13", "Invalid operation symbol placement - start")
    e.verbose = lambda args: "The regular expression reader encounter on symbol: \'" + args[0] + "\', that is one on the following symbols at the beginning of the RE { '?' , '+' , '*' , '.' , '|' }"
    lib.library.append(e)
    
    # e14 args: 0 - first symbol that was encountered
    #           1 - second symbol thet was encountered
    e = Error("e14", "Invalid operation sybol placement - neighbour")
    e.verbose = lambda args: "Pair: '" + args[0] + "', '" + args[1] + "' of the following symbols were encountered next to each { '.' , '|' } other"
    lib.library.append(e)

    # e15
    e = Error("e15", "Invalid operation symbol placement - pharenthesis")
    e.verbose = lambda args: "One of the following was placed after ‘(‘ symbol { '?' , '+' , '*' , '.' , '|' } or one of the following was placed before ‘)’ symbol { '.' , '|' }"
    lib.library.append(e)

    # e16 args: 0 - repetition sybol
    #           1 - non-repetition symbol
    e = Error("e16", "Invalid operation symbol placement - neighbour2")
    e.verbose = lambda args: "The repetition symbol: '" + args[0] + "', was encountered after non-repetition symbol: '" + args[1] + "'."
    lib.library.append(e)

    # e17 
    e = Error("e17", "Repetition operators close to each other")
    e.verbose = lambda args: "Pair of the following symbols were encountered next to each other what can cause unexpected results { '?' , '+' , '*' } and deadloop"
    lib.library.append(e)

    # Strings Errors
    # e30 args: 0 - encountered character
    e = Error("e30", "Not defined character in String file")
    e.verbose = lambda args: "The strings contains character: '" + args[0] + "', that is not a number or a letter"
    lib.library.append(e)

    # Other Errors
    # e98 args: 0 - message
    e = Error("e98", "I/O Error")
    e.verbose = lambda args: "There was an error with file I/O: " + args[0] + "."
    lib.library.append(e)

    # Warnings 

    # Conversion Warnings
    # w10
    e = Error("w10", "RE Whitespace")
    e.verbose = lambda args: "The regular expression contains whitespace character at the end, anything that is placed after that character will not be read"
    lib.library.append(e)

    # String Warnings
    # w30
    e = Error("w30", "Whitespace argument")
    e.verbose = lambda args: "One of the Strings is a whitespace"
    lib.library.append(e)

    # w80 args: 0 - filename
    e = Error("w80", "Overwrite Warning")
    e.verbose = lambda args: "One of the input files is the same as the output file: \"" + args[0] + "\"."
    lib.library.append(e)

    return lib

if __name__ == "__main__":
    # Printing error library for debug purposes
    for e in get_error_lib().library:
        print(e.code + " " + e.name)
        print(e.what_short(10))
        print(e.what_long(20, ["arg0", "arg1", "arg2"]))