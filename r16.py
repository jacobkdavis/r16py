#!/usr/bin/python3

import subprocess
import datetime
import argparse
import glob
import os.path


### config

masterfolder = "/h/audio/masters/"
sourcefolder = "/media/sdcard/"
copycmd = "rsync -t --progress"
defaultdays = "7"


### check folder setup

if(not masterfolder or not os.path.isdir(sourcefolder)):
    exit("Missing or invalid master / destination folder")

if(not sourcefolder or not os.path.isdir(sourcefolder)):
    exit("Missing or invalid source folder")


### projects

def projects(args):
    # stub function, redirect to project list
    projects_list(args)

def project_getname(folderpath):
    proj = os.path.basename(os.path.normpath(folderpath))
    
    # project name is held in PRJDATA.ZDT, 8 bytes long starting at byte 52
    
    projfile = folderpath + "/PRJDATA.ZDT"
    
    if(os.path.isfile(projfile)):
        f = open(projfile, 'rb')
        f.seek(52)
        projname = f.read(8).decode("utf-8")
        
        return(projname)


def projects_list(args):
    
    print("Projects in " + sourcefolder + ":")
    
    for folderpath in glob.iglob(sourcefolder + 'PROJ*/'):
        
        proj = os.path.basename(os.path.normpath(folderpath))
        
        projname = project_getname(folderpath)
        
        if(projname):
            print(proj + " - " + projname)


### masters

def masters(args):
    
    daysval = args.list or args.download
    
    if(daysval):    
        now = datetime.datetime.now()
        ago = datetime.timedelta(days=daysval)
        

        for filepath in glob.iglob(sourcefolder + 'PROJ*/AUDIO/MASTR*.WAV'):
            filename = os.path.basename(filepath)
            
            projid = os.path.basename(os.path.dirname(( os.path.abspath(os.path.join(filepath,"..")) )))
            
            projname = project_getname(sourcefolder + projid) or ""
            
            fmtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            
            if(fmtime > (now - ago)):
                print(projid + " (" + projname + ") - " + filename + " - " + str(fmtime))
                
                if(not projname):
                    projname = projid
                    
                destfilename = projname.strip() + "-" + filename
                
                if(args.download):
                    print("Copying " + filepath + " to " + masterfolder + destfilename)
                    #os.pat
                    
                    cmd = copycmd + " " + filepath + " " + masterfolder + destfilename
                    subprocess.call(cmd.split())
                
                    print("\n")
    else:
        parser_masters.print_help()
    

### parse cli arguments

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--source", help="source / sd card folder", default=sourcefolder)
parser.add_argument("-m", "--master", help="destination / master folder", default=masterfolder)

subparsers = parser.add_subparsers(help='sub-command help', dest='cmd', title="commands")
subparsers.required=True

# projects subcommand

parser_projects = subparsers.add_parser('projects', aliases=['p'], help='project folders')
parser_projects.add_argument("-l", "--list", action="store_true", help="list all projects")
parser_projects.set_defaults(func=projects)

# masters subcommand

parser_masters = subparsers.add_parser('masters', aliases=['m'], help='master audio files')
parser_masters.add_argument("-l", "--list", nargs='?', const=defaultdays, type=int, help="list recent master files in the last # days (default 7)")
parser_masters.add_argument("-d", "--download", nargs='?', const=defaultdays, type=int, help="download recent master files in the last # days (default 7)")
parser_masters.set_defaults(func=masters)

args = parser.parse_args()

args.func(args)

