
import logging
import os
import sys
from optparse import OptionParser

from kokki.kitchen import Kitchen

def build_parser():
    parser = OptionParser(usage="Usage: %prog [options] <command> ...")
    parser.add_option("-f", "--file", dest="filename", help="Look for the command in FILE", metavar="FILE", default="kitchen.py")
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true")
    return parser

def main():
    parser = build_parser()
    options, args = parser.parse_args()
    if not args:
        parser.error("must specify at least one command")

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    path = os.path.abspath(options.filename)
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    if path not in sys.path:
        sys.path.insert(0, path)

    if os.path.isdir(options.filename):
        files = [os.path.join(path, f) for f in sorted(os.listdir(path)) if f.endswith('.py')]
    else:
        files = [options.filename]

    globs = {}
    for fname in files:
        with open(fname, "rb") as fp:
            source = fp.read()
        exec compile(source, fname, 'exec') in globs

    kit = Kitchen()
    roles = []
    for c in args:
        try:
            roles.append(globs[c])
        except KeyError:
            sys.stderr.write("Function for role '%s' not found in config" % c)
            sys.exit(1)
    for r in roles:
        r(kit)
    kit.run()

if __name__ == "__main__":
    main()
