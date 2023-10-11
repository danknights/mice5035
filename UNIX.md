
# MiCE 5035 UNIX Command-line Guide

These are some of the more commonly used UNIX commands.

### scroll through your command history
```
<up/down arrow>
```

### kill the current process (or delete what you have written on the command line)
```
<control>-c
```

### search your command history
```
<control>-r (then type the search string)
```

### clear your screen
```
clear
```

### change into your “home” directory
```
cd
```

### switch groups if you have a research lab group also
This makes sure you're not using your lab's computing allotment
This is only if you already have an MSI account through a research lab.
```
newgrp mice5035
```


### list the contents of this directory
```
ls
```

### list the contents of the parent directory
```
ls ..
```

### list the contents of some other directory
```
ls /path/to/other/directory
```

### print out the full “path” to this directory. Also called the "absolute path".
```
pwd
```

### make a new directory (aka folder) for your programs (binaries)
```
mkdir bin
```

### make sure it got created
```
ls
```

### change into the “bin” directory
```
cd bin
```

### change back to the "parent" directory (the one just above this in the file system)
```
cd ..
```

### unzip a file
```
unzip zippedfile.zip
```

### remove a file
```
rm unwantedfile.txt
```

### list the number of lines, words, and characters in a file:
```
wc filename.txt
```


### remove a directory
```
rm -r unwanteddirectory
```

### view the first 10 lines of a file
```
head myfile.txt
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
```
cut -f 1-3 -d myfile.txt | head 
```

### scroll through the first 3 columns of the whole file (enter `q` to exit)
```
cut -f 1-10 -d "," myfile.txt | less
```

### scroll through the whole file
```
less myfile.txt
```

### make a copy of a file
```
cp file1.txt file2.txt
```

### copy a file to the current directory (`.` means current directory)
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

### kill a command that is running
```
<ctrl>-c
```

### search a file for a string or word. e.g. print out all lines that have a ">" character:
```
grep ">" input.fna
```

### print out all lines that DO NOT have a ">" character:
```
grep -v ">" input.fna
```

### count all lines that have a ">" character:
```
grep -c ">" input.fna
```

### start a "screen" session (like opening a tab, conceptually)
```
screen
```

### start another screen "tab" (like having multiple tabs open)
```
<ctrl>-a d
```

### move to the next screen "tab"
```
<ctrl>-a n
```

### move to the previous screen "tab"
```
<ctrl>-a p
```

### terminate/log out from a commandline session or screen session
```
<ctrl>-d
```

### temporarily detach from a screen session (don't hold ctrl after the `a`)
```
<ctrl>-a d
```

### re-attach to a screen session
```
screen -Dr
```
