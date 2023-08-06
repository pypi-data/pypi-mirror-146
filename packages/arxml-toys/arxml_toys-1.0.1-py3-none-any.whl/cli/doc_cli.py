import getopt
import sys
import os
from typing import List
from lib.arxml2xml import ARXML2Doc

from lib.utils import backup_original_file

def _usage(error: str):
    if error != "":
        print(error)
    print("arxml2xml [-a|--arxml name][-d name][-x|--xml name][-h|-help]")
    print("Remove or update the uuid from the specific arxml")
    print("   -a|--arxml name : To specify the file name of arxml")
    print("   -d name         : To specify the path name of arxml")
    print("   -x|--xml name   : The filename of SWC xml")
    print("   -h|--help       : Show the help information.")
    sys.exit(2)

def _parse_path(arxml_path: str, arxml_files: List[str]):
    for root, _, files in os.walk(arxml_path):
        path = root.split(os.sep)
        #print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            #print(len(path) * '---', file)
            if (os.path.splitext(file)[1] == ".arxml"):
                filename = os.path.join(root, file)
                arxml_files.append(filename)
                #print(filename)
    
def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "ha:d:x:", ["xml", "help", "arxml"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        _usage("")

    arxml_files = []
    swc_file = ""
    
    for o, arg in opts:
        if o in ("-a", "--arxml"):
            arxml_files.append(arg)
        elif o in ("-x", "--xml"):
            swc_file = arg
        elif o in ("-d"):
            _parse_path(arg, arxml_files)
        elif o in ("-h", "--help"):
            _usage("")
        else:
            assert False, "unhandled option"

    if len(arxml_files) == 0:
        _usage("Please enter the arxml filename")
    elif swc_file == "":
        _usage("Please enter the SWC xml file name")

    try:
        backup_original_file(swc_file)
        app = ARXML2Doc()
        app.convert_arxml_2_swc_xml(arxml_files=arxml_files, xml_file=swc_file)
        

    except Exception as e:
        # print(e)
        raise (e)