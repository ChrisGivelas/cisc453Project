#CISC 453 Project

Our project was developed and tested in python 3.6. (https://www.python.org/downloads/)

The main dependencies for this project are keras, tensorflow, Numpy (included with keras), and matplotlib.

###Method 1

The simplest way of installing all the dependencies is by using pip, a package manager for python.
Pip comes installed with python 3.4 or greater. Ensure that the the location of pip is on your
PATH.

run the following commands to fully download all of the required dependencies:

'pip install keras'
'pip install tensorflow'
'pip install matplotlib'

After that, you should be able to run our software by typing "python main.py" from the command
line from within this project's directory.


###Method 2

If you prefer to not install keras, tensorflow, matplotlib, and their associated dependencies
directly onto your system, you can use use a virtual environment to isolate these
packages in a known directory.

'virtualenv' is a python package in itself that you can install using pip:
'pip install -U pip virtualenv'

To create a virtualenv, create a new directory with a name of your choosing,
and then run 'virtualenv ./directoryname' to setup the environment. Each virtual environment
will have its own copy of the python interpreter. https://www.tensorflow.org/install/pip provides
great documentation on this entire process.

To start the virtualenv, find the 'activation script' in the 'Scripts' directory which
is associated with your OS.

After that, install all of the dependencies mentioned in "Method 1" above in the same way, and then
move all files from our software to your virtual environment.


============================================

To run our software, open up the command line to the location of main.py, and type
"python main.py".

Several statements will appear on the command line asking the user for input:
- Training episodes are the number of epochs in this simulation. Each episode
ends once it complete the specified number of time steps, or when all plants die
- Time steps are the number of individual watering's that occur through out a training
episode
- Number of plants is the number of plants used in this simulation

At the end of the training, a new directory will be created (in the same directory as main.py) called "plots", and this directory
will store line graphs containing information about each plant in the simulation. They can be used to verify whether
the training process was a success or not.


