## Guide to installing SHI7
Note: you only need to follow these steps once. 

We will download the code to run the `shi7` program into our own local directory, and we will tell our UNIX operating system where to find the code in the future. Then when we log in to MSI in the future, the operating system will be able to run `shi7`. This is a way to install software on LINUX systems without having administration privileges.

```bash
# change into your course “home” directory
cd /home/mice5035/<yourusername>

# list the contents of this directory, just for fun
ls

# print out the “path” to this directory, just for fun
pwd

# make a new directory (aka folder) for your programs (binaries)
mkdir bin

# make sure it got created
ls

# change into the “bin” directory
cd bin

# download the shi7 installation folder
wget https://github.com/knights-lab/shi7/releases/download/v0.9.9/shi7_0.9.9_linux_release.zip

# unzip it (but don’t type the whole filename; type “shi” then hit <tab> to auto-complete.
# always do that!)
unzip shi7_0.9.9_linux_release.zip

# remove the unneeded zip file
rm shi7_0.9.9_linux_release.zip

# tell the operating system where to find the shi7 programs next time you log in
# by adding the path to this directory to your system “PATH” variable
# we will send the following text to your ".bash_profile" file in 
# your official home directory. This will be loaded every time you log in in 
# the future. You do not need to run this command again the next time you log in.

# BE SURE TO FILL IN YOUR USERNAME where it says "<username>".
echo "PATH=\$PATH:/home/mice5035/<username>/bin" >> ~/.bash_profile; source ~/.bash_profile

# test that shi7.py runs
shi7.py -h

# change back to your course directory
cd /home/mice5035/<yourusername>

# get the course repository, if you have not yet done this.
git clone https://github.com/danknights/mice5035.git
```
