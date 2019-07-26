
#!/usr/bin/env python3
import argparse
import os
import stat
import re

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

args = ""
tabLength = 4
def preprocessor():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--include", action="store_true", default=False, help="Include hidden files")
    parser.add_argument("-a", "--access", action="store_true", default=False, help="View access status of files")
    parser.add_argument("-r", "--regex", help="Regex Expression to search")
    parser.add_argument("dir", nargs='?', default=os.getcwd(), help= "Path of the directory")
    args = parser.parse_args()

class Coloring:
    @staticmethod
    def coloredFolder(name):
        return bcolors.BLUE + name + '/' + bcolors.ENDC
    
    @staticmethod
    def coloredExecutable(name):
        return bcolors.GREEN +name + bcolors.ENDC
    
    @staticmethod
    def coloredAccess(name):
        return bcolors.UNDERLINE +name + bcolors.ENDC

    @staticmethod
    def colored(name, path):
        if os.path.isdir(path):
            return Coloring.coloredFolder(name)
        elif os.access(path, os.X_OK):
            return Coloring.coloredExecutable(name)
        else:
            return name


ongoing = set()
class Filex:
    def __init__(self, path, name, depth = 0):
        assert os.path.lexists(path), "{} path does not exists".format(path)
        self.path = path
        self.depth = depth
        self.name = name
            
    def printAdjusted(self, str, endl= '', fin='-'):
        for i in range(self.depth-1):
            if ongoing.__contains__(i):
                print('|', end='')
            else:
                print(' ', end='')
            print(" " * (tabLength-1), end = '' )
        if self.depth > 0:
            print("|" + fin * (tabLength-1), end='' )
        print(str, end = endl)
        
    @staticmethod
    def find(path, name, regex):
        # print('regex', path, regex)
        if re.search(regex, name):
            # print('regex', path, regex)
            return True
        if os.path.isdir(path):
            files = os.listdir(path) 
            if not args.include:
                files = [x for x in files if len(x)>0 and x[0] != '.']
            for file in files:
                if Filex.find( os.path.join(path,file), file, regex ):
                    return True
        return False
        


    def print(self):
        if len(args.regex) != 0:
            if not Filex.find(self.path, self.name, args.regex):
                return
        self.name = Coloring.colored(self.name, self.path)
        if args.access:
            self.name = self.name + ' '* tabLength + Coloring.coloredAccess( oct(stat.S_IMODE(os.lstat(self.path).st_mode))[2:] )
        self.printAdjusted(self.name, '\n')

        if os.path.isdir(self.path):
            files = os.listdir(self.path) 
            if not args.include:
                files = [x for x in files if len(x)>0 and x[0] != '.']
            files.sort()
            for i, file in enumerate(files):
                if i != len(files)-1:
                    ongoing.add(self.depth)

                Filex( os.path.join(self.path,file), file,  self.depth+1).print()

                if i != len(files)-1:
                    ongoing.remove(self.depth)

if __name__ == '__main__':
    preprocessor()
    # print(args)
    Filex(args.dir,args.dir).print()
