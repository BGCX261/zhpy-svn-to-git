#!/usr/bin/python
# -*- coding: utf-8 -*-

"""zhpy command line tool

This is the MIT license:
http://www.opensource.org/licenses/mit-license.php

Copyright (c) 2007 Fred Lin and contributors. zhpy is a trademark of Fred Lin.

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to 
deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.
"""

import os
import sys
from optparse import OptionParser
from release import version
from zhpy import annotator, convertor, try_run

def commandline():
    """zhpy, the python language in chinese

Accept options:
    -i --input:
        speficy the input source
    -o --output:
        speficy the output source
    -p --python:
        compile to python and run
    -c --cmp:
        input raw zhpy source and run
    -e --encoding:
        specify the encoding
    --info:
        zhpy information
    -v --verbose:
        show zhpy progress in detail
    --tw:
        convert python to twpy
    --cn:
        convert python to cnpy

help:
    get information:
        zhpy --info

    interpreter usage:
        zhpy [--tw | --cn]

    command usage:
        zhpy [-i | -p] input [-o] [output] [-e] [encoding] [-v]

    ::
    
        $ zhpy input.py (.twpy, .cnpy) [arguments]
        $ zhpy -i input.py (.twpy, .cnpy)
        $ zhpy -i input.py -o output.py (.twpy, .cnpy)
        $ zhpy -p input.py   

    script usage:
        zhpy [-c] source [-e] [encoding] [-v]

    convertor usage:
        zhpy [--tw | --cn] input.py [-v]
    
    ::
    
        $ zhpy --tw input.py [-v]
        $ zhpy --cn input.py [-v]

    """
    argv = sys.argv[1:]
    os.chdir(os.getcwd())
    
    source = None
    target = None
    encoding = None
    raw_source = None
    verbose = False
    python = False
    tw = False
    cn = False
    # run as interpreter
    if len(argv) == 0:
        from interpreter import interpreter
        interpreter()
        sys.exit()
    # run as script
    # not accept any option
    elif not argv[0].startswith('-'):
        source = argv[0]
        sys.argv = argv
    # run as command
    elif len(argv)==1:
        if argv[0] == '--info':
            from info import info
            info()
            sys.exit()
        elif argv[0] == '-h' or argv[0] == '--help':
            print commandline.__doc__
            sys.exit()
        # run as native interpreter
        elif argv[0] == '--tw':
            from interpreter import interpreter
            interpreter('tw')
            sys.exit()
        elif argv[0] == '--cn':
            from interpreter import interpreter
            interpreter('cn')
            sys.exit()
        else:
           print commandline.__doc__
           sys.exit()
    # accept "-c -e -v"
    elif len(argv)>=2:
        if argv[0] == '-c' or argv[0] == '--cmp':
            raw_source = argv[1]
            del(argv[:2])
            if len(argv)>=2 and (argv[0] == '-e' or argv[0] == '--encoding'):
                encoding = argv[1]
                del(argv[:2])
                if (len(argv)!=0) and (argv[0] == '-v' or argv[0] == '--verbose'):
                    verbose = True
        # python to twpy
        elif argv[0] == '--tw':
            source = argv[1]
            filename = os.path.splitext(source)[0]
            del(argv[:2])
            tw = True
            target = "v_"+filename+".twpy"
            if (len(argv)!=0) and (argv[0] == '-v' or argv[0] == '--verbose'):
                verbose = True
        # python to cnpy
        elif argv[0] == '--cn':
            source = argv[1]
            filename = os.path.splitext(source)[0]
            del(argv[:2])
            cn = True
            target = "v_"+filename+".cnpy"
            if (len(argv)!=0) and (argv[0] == '-v' or argv[0] == '--verbose'):
                verbose = True
        # accept "-i -o -e -v" or "-p -e" or "-c -e -v"
        elif argv[0] == '-i' or argv[0] == '--input':
            source = argv[1]
            del(argv[:2])
            if (len(argv)!=0) and (argv[0] == '-v' or argv[0] == '--verbose'):
                verbose = True
            if len(argv)>=2 and (argv[0] == '-e' or argv[0] == '--encoding'):
                encoding = argv[1]
                del(argv[:2])
                if (len(argv)!=0) and (argv[0] == '-v' or argv[0] == '--verbose'):
                    verbose = True
            if len(argv)>=2 and (argv[0] == '-o' or argv[0] == '--output'):
                target = argv[1]
                del(argv[:2])
                if len(argv)>=2 and (argv[0] == '-e' or argv[0] == '--encoding'):
                    encoding = argv[1]
                    del(argv[:2])
                    if (len(argv)!=0) and (argv[0] == '-v' or argv[0] == '--verbose'):
                        verbose = True
        elif argv[0] == '-p' or argv[0] == '--python':
            source = argv[1]
            filename = os.path.splitext(source)[0]
            del(argv[:2])            
            target = "n_"+filename+".py"
            python = True
            print "compile to python and run: %s"%("n_"+filename+".py")
            if (len(argv)!=0) and (argv[0] == '-v' or argv[0] == '--verbose'):
                verbose = True
            if len(argv)>=2 and (argv[0] == '-e' or argv[0] == '--encoding'):
                encoding = argv[1]
                del(argv[:2])
                if (len(argv)!=0) and (argv[0] == '-v' or argv[0] == '--verbose'):
                    verbose = True
    else:
        print commandline.__doc__
        sys.exit()
    #convert
    if raw_source:
        if verbose:
            print "run raw_source", raw_source
        annotator()
        if encoding:
            result = convertor(raw_source, verbose, encoding)
        else:
            result = convertor(raw_source, verbose)
        try_run(result)
        sys.exit()
    
    if encoding:
        print "encoding", encoding

    if source:
        if verbose:
            print "input", source
        # convertor
        if(tw or cn):
            if verbose:
                print "convert python code to",
            try:
                from pyzh import rev_annotator, python_convertor
                test = file(source, "r").read()
                if tw:
                    print "twpy"
                    rev_annotator('tw', verbose)
                    result = python_convertor(test, lang='tw')
                if cn:
                    print "cnpy"
                    rev_annotator('cn', verbose)
                    result = python_convertor(test, lang='cn')
            except Exception, e:
                print "zhpy Exception: you may input unproper source"
                if verbose:
                    print e
                sys.exit()
        else:
            try:
                test = file(source, "r").read()
                annotator()
                if encoding:
                    result = convertor(test, verbose, encoding)
                else:
                    result = convertor(test, verbose)
            except Exception, e:
                print "zhpy Exception: you may input unproper source"
                if verbose:
                    print e
                sys.exit()
    if target:
        if verbose:
            print "output", target
        file(target,"w").write(result)
        if python:
            try_run(result)
    else:
        try_run(result)

if __name__=="__main__":
    commandline()
