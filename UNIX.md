
# UNIX Command-line Guide

These are some of the more commonly used UNIX commands.

# BEGINNER commands

### scroll through your command history
```
<up/down arrow>
```

### kill the current process (or delete what you have written on the command line)
```
<control>-c
```

### change into your “home” directory
```
cd
```

### Find out what directory you are in.
```
pwd
```

### list the contents of the current directory/folder
```
ls
```

### list the contents of some other directory
```
ls /path/to/other/directory
```

### make a new directory (aka folder) for your programs (binaries)
```
mkdir bin
```

### make sure it got created
```
ls
```

### list the contents of a directory 
```
ls bin
```

### enter into the “bin” directory (cd means "change directory")
```
cd bin
```

### exit the "bin" directory
(change back to the "parent" directory, the one just above this in the file system)
```
cd ..
```

### remove a file
```
rm unwantedfile.txt
```

### remove a directory
```
rm -r unwanteddirectory
```

# INTERMEDIATE commands

### unzip a file
```
unzip zippedfile.zip
```

### list the number of lines, words, and characters in a file:
```
wc filename.txt
```

### view the first 10 lines of a file
```
head myfile.txt
```

### print an entire file to the screen (might be long)
```
cat filename.txt
```

### view the first 3 columns (fields) of a file, assuming tab delimiters
```
cut -f 1-3 myfile.txt
```

### view the first 3 columns (fields) of a file, assuming comma delimiters
```
cut -f 1-3 -d "," myfile.txt
```

### view the first 10 lines of the first 3 columns 
(note the use of `|` to pipe the output of one command to another)
```
cut -f 1-3 myfile.txt | head 
```

### view the first 20 characters of each line in a file
```
cut -c 1-20 myfile.txt
```

### view the first 20 characters of the first 10 lines in a file
```
cut -c 1-20 myfile.txt | head 
```

### scroll through a file (space bar jumps down a page, "b" jumps back a page)
```
less myfile.txt
```

### scroll through the first 3 columns of the whole file (enter `q` to exit)
(note again the use of `|` to pipe the output of `cut` to `less`)
```
cut -f 1-10 -d "," myfile.txt | less
```

### make a copy of a file
```
cp file.txt filecopy.txt
```

### copy a file to a directory
```
cp file.txt directory_name
```

### copy a distant file to the current directory (`.` means current directory)
```
cp /full/path/to/other/file.txt .
```

### make a copy of a directory
```
cp -r directory1 directory2
```

### mv (rename) a file
```
mv oldname.txt newname.txt
```

### see how large files are
```
du -hs *
```

### edit a file (exit with ctrl-x)
```
nano somefile.txt
```

### search a file for a string or word
(e.g. print out all lines that have a ">" character)
```
grep ">" input.fna
```

### search for lines that do _not_ match a pattern
(e.g. print lines that DO NOT have a ">" character)
```
grep -v ">" input.fna
```

### count all lines that have a ">" character:
```
grep -c ">" input.fna
```

# ADVANCED commands

## Using "Screen" to keep a session open
If you need to run something that will take a while, there are ways to keep an interactive computing session open on MSI. One way is to log in to a _specific_ login node (e.g. `ahl01`), open a "screen" session, and then start your interactive session. The screen session will stay open on the login node if you disconnect and connect again later. Here are the steps:

1. When you first connect to MSI, connect to a specific login node:
```bash
ssh username@ahl01.msi.umn.edu
```
2. Start a "screen" session (like opening a browser window, conceptually)
```
screen
```
3. Launch your compute node
```bash
srun ...
```
4. When you need to log off temporarily, detach from the screen session (don't hold ctrl after the `a`)
```
<ctrl>-a d
```
Then exit the login node with `<ctrl>-d` or `exit`.
5. When ready to log back on, connect to the same login node:
```bash
ssh username@ahl01.msi.umn.edu
```
6. Re-attach to the screen session
```
screen -Dr
```

Now you are back on the compute node, right where you left off. If you had a command running, it will have continued running in the background.

## Other helpful screen commands
### start another screen "window" (like opening another tab in a browser)
```
<ctrl>-a c
```

### move to the next screen "tab"
```
<ctrl>-a n
```

### move to the previous screen "tab"
```
<ctrl>-a p
```

### terminate/permanently close a commandline session or screen session
```
<ctrl>-d
```

### search your command history
```
<control>-r (then type the search string)
```

### clear your screen
```
clear
```
