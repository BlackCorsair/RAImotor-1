# Virtualenv Guide
## Installation
### Ubuntu
```
sudo apt install python3 python3-virtualenv
```
### Pip
```
sudo -H pip install virtualenv
```
## Usage
### Start a virtual environment
To start a default virtual environment, just write in the console:
```
virtualenv <dir-name>
```

To specify a python version:
```
virtualenv <dir-name> -p pythonX
```
Where 'X' is the version (_python_ for python 2.X and _python3_ for python3.X)

When a virtual environment is started, it creates a directory with al the executables needed and some tools like _pip_, following the next tree architecture:
```
venv
├── bin
├── include
├── lib
└── pip-selfcheck.json
```

* **bin**: it includes all the executables, like python or pip
* **include**: contains the modules
* **lib**: contains the libraries

### Activate the virtualenv
```
source <dir-name>/bin/activate
```

Here is the difference in zsh in a non-activated environment vs an activated one:
```
╭─jhevia@T470 ~/Documents/University/RAI/RAIvectorial  ‹develop*› 
╰─$ 
```
_non-activated_

```
(venv) ╭─jhevia@T470 ~/Documents/University/RAI/RAIvectorial  ‹develop*› 
╰─$ 
```
_activated, notice the (venv) at the beginning_

_To deactivate the virtual environment just type **deactivate**_

### Make your python programs to execute always with the environment
First, at the beginning of your python file, write the next line:
```
#!/venv/bin/python
```
or
```
#!venv/bin/python3
```

Next, you'll want to make executable the python file:
```
chmod a+x python-program.py
```

Now you can execute it with only **./python-program.py**

