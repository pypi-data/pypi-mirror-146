# Installation                                                                                                                                                                                                                                                
## Prerequisites
The cfde-submit command requires Python 3 and package manager "pip". Pip is included by default with Python 3.4 and later.  For more information on installation, please refer to [https://www.python.org](https://www.python.org).

## Create a Virtual Environment
To avoid potential conflicts, we recommended installing `cfde-submit` from within a Python 3 virtual environment. A virtual environment is an isolated Python installation with its own set of packages separate from what has been previously installed on your system. Additional information about virtual environments can be found at [https://docs.python.org/3/tutorial/venv.html](https://docs.python.org/3/tutorial/venv.html).

The steps below will walk you through the process of creating a new virtual environment called cfde_venv.

 1. To create a new environment, run the command: `python3 -m venv cfde_venv`
 2. To start the environment, run the command: `source cfde_venv/bin/activate`
 3. You should notice the string "(cfde_venv)" prepended to your shell prompt, indicating the virtual environment is running
 4. To exit the environment, run the command `deactivate` 

Alternatively, you can also use conda to create a new virtual environment.

1. Create a new conda environment: `conda create --name cfde_venv python`
2. Activate the environment: `conda activate cfde_venv`
3. Successful activation of the virtual environment will result in the update from "(base)" to "(cfde_venv)" in front of your shell prompt
4. To exit the environment run: `conda deactivate`

## Install Git
`cfde-submit` has the ability to read data from github repositories. To avoid any git-related errors, please install the git on your system. On Ubuntu, this can be done by running `sudo apt update` and `sudo apt install git`.

## Install cfde-submit
The most recent release of `cfde-submit` can be installed via pip. The commands below should be run while the `cfde_venv` environment is active.

Please ensure pip is up to date by running the command: `pip3 install --upgrade pip`. Next, run the command: `pip3 install cfde-submit`. This will install `cfde-submit` and all other required packages. These packages will install into your virtual environment and be added to your path.

To verify the installation has succeeded, run the command `cfde-submit` to see the list of available commands.

## Update cfde-submit
To update the cfde-submit package to the latest version, run the commands below.

```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade cfde-submit
```

