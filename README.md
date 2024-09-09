# Elevator simulator

This is a work in progress, not ready for a public review.

I wanted to:

* play with elevator simulation
* play with using [FastAPI](https://fastapi.tiangolo.com/) for microservices

It also appeared that [ZeroMQ](https://zeromq.org/) is a perfect fit to make
things work together.

BTW [simpy](https://simpy.readthedocs.io/en/latest/) is awesome and is highly
recommended.  Not used in this project.


More [documents](./docs/)

## Prerequisites

### 0MQ

Follow [documentation](https://zeromq.org/download/) to install:

For MacOS:
```sh
brew install zmq
```

For Linux:
```sh
sudo apt-get install libzmq3-dev
```

To verify install:
```
> python
Python 3.10.14 (main, Mar 19 2024, 21:46:16) [Clang 15.0.0 (clang-1500.3.9.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import zmq
>>> print(f"Current libzmq version is {zmq.zmq_version()}")
Current libzmq version is 4.3.5
>>> print(f"Current  pyzmq version is {zmq.__version__}")
Current  pyzmq version is 26.2.0
>>> exit()
```

### Python libs

Are handled using virtual environment

## Unit Tests

To run all:
```sh
make tests
```

To run unit test:
```sh
python -m unittest tests/simulation_test.py
```

to find out if fastapi is running:
```sh
ps ax|grep fastapi
```

To find out who binds port 5556:
```
sudo lsof -i4 |grep LISTEN|grep 5556
```

## How to use it

```sh
fastapi run simultons/simulation.py
```

To watch the simulton processes:

1. use `ps` to identify the pid of the shell;
2. then

```
watch -c -n 0.1  pstree -p <pid> -Ut
```

## TODOs

* simultons to read from the zmq message queue

DONE:

* use [httpx](https://www.python-httpx.org/advanced/clients/) instead of request
