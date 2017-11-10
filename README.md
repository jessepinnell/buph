# XRSRV - eXeRcise SeRVer
> Workout and physical fitness database and software library

XRSRV is intended to be a fully open-source back-end database and library for physical fitness routines and workout
management software.  However, for now it will serve as a place to share scripts and utilities for generating workouts in HTML format to
be printed and put on a clipboard.  Eventually, the idea is to have both a fully functional web and a local API which will ease writing user
interfaces on any number of devices.  We'll see how far it gets.

While there are many examples of mature projects and commercial products that provide essentially the same thing, XRSRV is more focused on 
versatility, re-use, and its availability as an entirely open-source product.  It's also a good software exercise, no pun intended.

This project will be written in a platform-independent manner (assuming someone will port it to Windows; we'll do our
best from the Linux side of the development), and will follow strict coding and formatting standards.

## Installation

The installer is incomplete but the project uses the CMake build system and it can be used in place.  CMake should
detect and at least complain about some or all missing dependencies.  Note that it is written using python 3, so the python 3
version of libraries are required.  Pylint3 is required for the lint target.

To build XRSRV under Linux:

```
$ git clone https://github.com/jessepinnell/xrsrv.git
```

```
$ mkdir xrsrv-build
```

```
$ cd xrsrv-build
```

```
$ cmake ../xrsrv
```

```
$ make
```

```
$ make test
```

```
$ make lint
```

## Usage example

Functionality is currently very limited, but the basic exercise renderer script can be run from the build directory:

```
$ export PYTHONPATH=$(dirname `pwd`)/xrsrv/python
```

```
$ python3 -B ../xrsrv/python/apps/exercise_renderer.py
```

```
usage: ../xrsrv/python/apps/exercise_renderer.py [exercises database file] [number of routines]
```

```
$ python3 -B ../xrsrv/python/apps/exercise_renderer.py python/tests/exercise.db 12 > /tmp/output_file.html
```

## Development setup

Same as installation steps above for now.

## Release History

* 0.1
    * Basic architecture designed
    * Project builds
    * Pylint is enabled
    * Unit testing framework works
    * Simple apps scripts exist
    * Back-end exercise database is partially populated

* 0.0.1
    * Project is created and has some basic scripts

## Meta

Jesse Pinnell – jesse@vapid.io

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/jessepinnell](https://github.com/jessepinnell/)

## Contributing

I'm still in the process of setting up the project and designing the overall architecture.  Please stay tuned.
