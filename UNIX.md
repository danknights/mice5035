
# MiCE 5035 UNIX Command-line Guide

These are some of the more commonly used UNIX commands.

### change into your “home” directory
```
cd
```

### list the contents of this directory
```
ls
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

### list the contents of another directory inside the current directory
```
ls somedirectory
```

### list the contents of another directory inside the parent directory
```
ls ../someotherdirectory
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

### start a "screen" session
```
screen
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
screen -r
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
