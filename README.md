# r16py

Command-line file management utility for Zoom R16 multitrack recorders for linux, written in Python.

## Initial setup

- Download copy of script
- Edit script to set configuration variables
-- masterfolder = local folder for storage of mastered .wav files
-- sourcefolder = path to the zoom sd card or usb device 
-- copycmd = set to use rsync by default to show progress while copying larger files, but you could also change this to "cp" when rsync isn't available
-- defaultdays = default setting for how 
- Set script to executable (chmod +x r16.py) and run via "r16.py", or run via "python r16.py"

## Basic usage

```
usage: r16.py [-h] [-s SOURCE] [-m MASTER] {projects,p,masters,m} ...

optional arguments:
-h, --help            show this help message and exit
-s SOURCE, --source SOURCE
source / sd card folder
-m MASTER, --master MASTER
destination / master folder

commands:
{projects,p,masters,m}
sub-command help
projects (p)        project folders
masters (m)         master audio files

```

## Projects (zoom multi-track projects)

```
usage: r16 projects [-h] [-l]

optional arguments:
-h, --help  show this help message and exit
-l, --list  list all projects
```

## Masters (mastered audio .wav files)

```
usage: r16 masters [-h] [-l [LIST]] [-d [DOWNLOAD]]

optional arguments:
-h, --help            show this help message and exit
-l [LIST], --list [LIST]
list recent master files in the last # days (default 7)
-d [DOWNLOAD], --download [DOWNLOAD]
download recent master files in the last # days (default 7)
```
