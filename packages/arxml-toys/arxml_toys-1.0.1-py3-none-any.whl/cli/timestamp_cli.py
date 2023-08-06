import re
import getopt
import sys

from lib.utils import backup_original_file

def _usage(error: str):
    if error != "":
        print(error)
    print("arxml_timestamp [-a|--arxml name][-h|-help]")
    print("Remove the timestamp from the specific arxml")
    print("   -a|--arxml name : The filename of arxml")
    print("   -h|--help       : Show the help information.")
    sys.exit(2)
    
def timestamp_remove(filename):
    lines = []
    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = re.sub(r'\s+T\=\"([\w\-\:\+])+"', '', line)
            lines.append(line)

    with open(filename, 'w', encoding="utf-8") as outfile:
        outfile.writelines(lines)
    
def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "ha:", ["help", "arxml"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        _usage("")

    filename = ""
    for o, arg in opts:
        if o in ("-a", "--arxml"):
            filename = arg
        elif o in ("-h", "--help"):
            _usage("")
        else:
            assert False, "unhandled option"

    if filename == "":
        _usage("Please enter the arxml filename")

    try:
        backup_original_file(filename)
        timestamp_remove(filename)

    except Exception as e:
        # print(e)
        raise (e)