#!/usr/bin/python3

from argparse import ArgumentParser
import random, sys, string

"""
Write a random permutation of the input lines to standard output.

With no FILE, or when FILE is -, read standard input.

Mandatory arguments to long options are mandatory for short options too.

  -e, --echo                treat each ARG as an input line
  -i, --input-range=LO-HI   treat each number LO through HI as an input line
  -n, --head-count=COUNT    output at most COUNT lines
  -r, --repeat              output lines can be repeated
      --help     display this help and exit
"""

class shufline:
    def __init__(self, filename, lines):
        # initialize with a file or lines
        if (filename):
            f = open(filename, 'r')
            self.lines = f.read().splitlines()
            f.close()
        else:
            self.lines = lines

    # shuffle
    def shuffle(self):
        random.shuffle(self.lines)
        return self.lines

    # number of lines
    def length(self):
        return len(self.lines)

def shuffle(generator, count, headcount, repeat, newline):
    # keep shuffling if count == 0, repeating, or there's more to shuffle 
    while ((count == 0 or repeat) and (generator.length() > 0)):
        for line in generator.shuffle():
            sys.stdout.write(line + ('\n' if newline else ''))
            count += 1
            if (headcount != -1 and count >= headcount):
                repeat = False
                break                                                                   

def main():
    usage_msg = """
    %(prog)s [OPTION]... [FILE]
    %(prog)s -e [OPTION]... [ARG]...
    %(prog)s -i LO-HI [OPTION]...

    Write a random permutation of the input lines to standard output.

    With no FILE, or when FILE is -, read standard input.

    Mandatory arguments to long options are mandatory for short options too.

    -e, --echo                treat each ARG as an input line
    -i, --input-range=LO-HI   treat each number LO through HI as an input line
    -n, --head-count=COUNT    output at most COUNT lines
    -r, --repeat              output lines can be repeated
    --help        display this help and exit                            
"""

    parser = ArgumentParser(usage=usage_msg)

    # arguments: e, i, n, r, or a file
    parser.add_argument('File', nargs='*', default=[], help="File which to permute line")
    parser.add_argument("-e", "--echo", action='store_true', help="treat each ARG as an input line")
    parser.add_argument("-i", "--input-range", action='store', help="treat each number LO through HI as an input line")
    parser.add_argument("-n", "--head-count", action='store', help="output at most COUNT lines")
    parser.add_argument("-r", "--repeat", action='store_true', help="output lines can be repeated")

    args, others  = (parser.parse_known_args(sys.argv[1:]))
    args = vars(args) # convert into dictionary            

    # extra args
    if (len(others) > 0):
        for a in others:
            if (len(a) > 2 and a[0] == '-' and a[1] == '-'):
                sys.stderr.write("shuf: unrecognized option '" + str(others[0]) + "'\n")
                return
            elif (a[0] == '-'):
                sys.stderr.write("shuf: invalid option '" + str(others[0]) + "'\n")
                return
            else:
                args['File'].append(a)

    # default values
    headcount = -1
    echo = False
    rng = False
    inp = False
    file = False
    count = 0
    lines = []

    # parsing through arguments
    for arg in args.items():
        match arg:
            case('echo', True):
                echo = True
                if (len(args['File']) != 0):
                    lines = args['File']
            case ('input_range', val):
                try:
                    if (val != None):
                        # negative input
                        if (len(val) > 0 and val[0] == '-'):
                            sys.stderr.write("shuf: invalid input range\n")
                            return
                        rng = True
                        r = val.split('-', 1)
                        # wrong split
                        if (len(r) != 2):
                            if (len(r) > 0):
                                sys.stderr.write("shuf: invalid input range: '" + str(val[0]) + "'\n")
                            else:
                                sys.stderr.write("shuf: invalid input range: '" + str(val) + "'\n")
                            return
                        # lower value
                        try:
                            small = int(r[0])
                        except:
                            sys.stderr.write("shuf: invalid input range: '" + str(r[0]) + "'\n")
                            return
                        # upper value
                        try:
                            large = int(r[1])
                        except:
                            sys.stderr.write("shuf: invalid input range: '" + str(r[1]) + "'\n")
                            return
                        # lower value > upper value
                        if (small > large):
                            sys.stderr.write("shuf: invalid input range: '" + str(val[0]) + "'\n")
                            return
                        # normal case
                        else:
                            lines = [(str(i)) for i in range(small, large + 1)]
                except:
                    sys.stderr.write("shuf: invalid input range: '" + str(val) + "'\n")
                    return
            case ('head_count', val):
                # given a value
                if (val != None):
                    try:
                        headcount = int(val)
                        # negative value
                        if (headcount < 0):
                            sys.stderr.write("shuf: invalid line count: '" + str(val) + "'\n")
                            return
                    except:
                        sys.stderr.write("shuf: invalid line count: '" + str(val) + "'\n")
                        return
            case('File', params):
                # no parameters, -, -e, -i
                if ((len(params) == 0 or (len(params) == 1 and params[0] == '-')) and (not args['echo'] and args['input_range'] == None)):
                    inp = True
                # no -e, -i
                elif (not args['echo'] and args['input_range'] == None):
                    file = True
                    # more than one parameter
                    if (len(params) > 1):
                        sys.stderr.write("shuf: extra operand '" + str(params[1]) + "'\n")
                        return

    # error handling
    if (echo and rng):
        sys.stderr.write("shuf: cannot combine -e and -i\n")
        return
    elif (rng and len(args['File']) > 0):
        sys.stderr.write("shuf: extra operand '" + str(args['File'][0]) + "'\n")
        return

    # reading input if necessary
    # if input and -n has a value
    if (inp and headcount != 0):
        lines = sys.stdin.read().splitlines()
    # if there is a file
    if (file):
        try:
            generator = shufline(args['File'][0], None)
            shuffle(generator, count, headcount, args['repeat'], True)
        except:
            sys.stderr.write("shuf: " + str(args['File'][0]) + ": No such file or directory\n")
            return
    # no file, just input
    else:
        generator = shufline(None, lines)
        shuffle(generator, count, headcount, args['repeat'], True)

if __name__ == "__main__":
    main()
