# PYSILICO: Prosilica AVT camera controller for Plico

 ![Python package](https://github.com/ArcetriAdaptiveOptics/pysilico/workflows/Python%20package/badge.svg)
 [![codecov](https://codecov.io/gh/ArcetriAdaptiveOptics/pysilico/branch/master/graph/badge.svg?token=GTDOW6IWDE)](https://codecov.io/gh/ArcetriAdaptiveOptics/pysilico)
 [![Documentation Status](https://readthedocs.org/projects/pysilico/badge/?version=latest)](https://pysilico.readthedocs.io/en/latest/?badge=latest)
 [![PyPI version][pypiversion]][pypiversionlink]



pysilico is an application to control [Allied AVT/Prosilica][allied] cameras (and possibly other GigE cameras) under the [plico][plico] environment.

[plico]: https://github.com/ArcetriAdaptiveOptics/plico
[travis]: https://travis-ci.com/ArcetriAdaptiveOptics/pysilico.svg?branch=master "go to travis"
[travislink]: https://travis-ci.com/ArcetriAdaptiveOptics/pysilico
[coveralls]: https://coveralls.io/repos/github/ArcetriAdaptiveOptics/pysilico/badge.svg?branch=master "go to coveralls"
[coverallslink]: https://coveralls.io/github/ArcetriAdaptiveOptics/pysilico
[allied]: https://www.alliedvision.com
[pypiversion]: https://badge.fury.io/py/pysilico.svg
[pypiversionlink]: https://badge.fury.io/py/pysilico



## Installation

### On client

On the client machine

```
pip install pysilico
```

### On the server

On the server machine install the proprietary driver for the camera you want to control. Currently only AVT/Prosilica camera are supported through Vimba

#### For AVT / Prosilica

First install Vimba (that comes with the camera, or download Vimba SDK from AVT website). Check that the Vimba installation is successful and that the camera is accessible by the server using VimbaViewer, the standalone application provided in Vimba SDK. You should be able to see the cameras in the network and stream images.

Then install the Vimba python wrapper. Check that the installation is successfull by running the provided example, like the one below:

```
(pysilico) lbusoni@argos:~/Downloads/Vimba_5_0/VimbaPython/Examples$ python list_cameras.py 
//////////////////////////////////////
/// Vimba API List Cameras Example ///
//////////////////////////////////////

Cameras found: 1
/// Camera Name   : GC1350M
/// Model Name    : GC1350M (02-2130A)
/// Camera ID     : DEV_000F3101C686
/// Serial Number : 02-2130A-06774
/// Interface ID  : eno2

(pysilico) lbusoni@argos:~/Downloads/Vimba_5_0/VimbaPython/Examples$ 
```


#### Install server
As a last step you always have to install the generic pysilico-server

```
pip install pysilico-server
```

The pysilico-server package installs also the client package.




## Usage

### Starting Servers

Starts the 2 servers that control one device each.

```
pysilico_start
```

### Using the GUI

Run `pysilico_gui`
  

### Using the client module 

In a python terminal on the client computer:

```
In [1]: import pysilico

In [2]: cam1= pysilico.camera('192.168.1.18', 7100)

In [3]: cam2= pysilico.camera('192.168.1.18', 7110)

In [4]: frames= cam1.getFutureFrames(10)
```

### Stopping pysilico

To kill the servers run

```
pysilico_stop
```

More hard:

```
pysilico_kill_all
```




## Administration Tool

For developers.


### Testing
Never commit before tests are OK!
To run the unittest and integration test suite cd in pysilico source dir

```
python setup.py test
```


### Creating a Conda environment
Use the Anaconda GUI or in terminal

```
conda create --name pysilico
```

To create an environment with a specific python version

```
conda create --name pysilico python=2.6
```


It is better to install available packages from conda instead of pip. 

```
conda install --name pysilico matplotlib scipy ipython numpy
```

### Packaging and distributing

See https://packaging.python.org/tutorials/distributing-packages/#

To make a source distribution

```
python setup.py sdist
```

and the tar.gz is created in ../dist


You can make a universal wheel 

```
python setup.py bdist_wheel 
```

The wheels are created in ../dist. I suppose one can delete 
pysilico/build now and distribute the files in ../dist


To upload on pip (but do you really want to make it public?)

```
twine upload ../dist/*
```
