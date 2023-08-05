import re
import getopt
import sys
import uuid

from lib.utils import backup_original_file

def _usage(error: str):
    if error != "":
        print(error)
    print("arxml_uuid [-a|--arxml name][--remove][-h|-help]")
    print("Remove or update the uuid from the specific arxml")
    print("   -a|--arxml name : The filename of arxml")
    print("   --remove        : Remove the UUID")
    print("   -h|--help       : Show the help information.")
    sys.exit(2)
    
def uuid_remove(filename):
    lines = []
    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = re.sub(r'\s+UUID\=\"([\w\-])+\"', '', line)
            lines.append(line)

    with open(filename, 'w', encoding="utf-8") as outfile:
        outfile.writelines(lines)

def uuid_update(filename):
    lines = []
    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            new_uuid = 'UUID="%s"' % str(uuid.uuid4())
            line = re.sub(r'UUID\=\"([\w\-])+\"', new_uuid, line)
            lines.append(line)

    with open(filename, 'w', encoding="utf-8") as outfile:
        outfile.writelines(lines)
    
def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "ha:", ["remove", "help", "arxml"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        _usage("")

    filename = ""
    is_remove = False
    for o, arg in opts:
        if o in ("-a", "--arxml"):
            filename = arg
        elif o in ("--remove"):
            is_remove = True
        elif o in ("-h", "--help"):
            _usage("")
        else:
            assert False, "unhandled option"

    if filename == "":
        _usage("Please enter the arxml filename")

    try:
        backup_original_file(filename)

        if (is_remove):
            uuid_remove(filename)
        else:
            uuid_update(filename)

    except Exception as e:
        # print(e)
        raise (e)