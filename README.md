# Elevator simulator

This is a work in progress, not ready for a public review.

I wanted to:

* play with elevator simulation
* play with using [FastAPI](https://fastapi.tiangolo.com/) for microservices

It also appeared that [ZeroMQ](https://zeromq.org/) is a perfect fit to make
things work together.

BTW [simpy](https://simpy.readthedocs.io/en/latest/) is awesome and is highly
recommended.  It is NOT used in this project.

More [documents](./docs/)

## Major Qs

These were distilled within hours...

### How do I programmatically start the FastAPI server?

Unfortunately, short answer is "it depends".
Because FastAPI is just an "ASGI app".  If this does not help, I'm with you.

#### Option 1: launch it using fastapi cli:

```
        '''
        start the FastAPI service process, returns service process pid
        '''
        command_line = [
            'fastapi', 'run', '--host', '127.0.0.1',
            '--port', str(9000), '--workers', str(1), 'app.py'
        ]
        self._popen = subprocess.Popen(
            command_line,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

```
#### Option 2: launch it using uvicorn programmatic API:

uvicorn is used y FastAPI by default anyway...

```
import fastapi
import uvicorn

host = '127.0.0.1'
port = 8000
app = fastapi.FastAPI()


@app.get('/hello')
async def hello():
    return {
        'message': 'hello world'
    }


def launch_uvicorn() -> None:
    '''
    Start FastAPI uvicorn app
    see also:
    https://bugfactory.io/articles/starting-and-stopping-uvicorn-in-the-background/
    '''
    uvicorn.run(app, host=host, port=port, workers=1, log_level='debug')
    return
```

### How do I programmatically shut the FastAPI server?

https://gist.github.com/BnJam/8123540b1716c81922169fa4f7c43cf0

1. define an endpoint to shut the server
2. When the endpoint is hit, create a background task to shut the server

```
@app.put(
    '/api/v1/simulation',
    response_model=SimulationResponse,
    status_code=202,
    responses={400: {"model": Message}})
async def put_simulation(req: SimulationRequest):
    '''
    Update the simulation state
    '''
    assert theSimulation is not None
    if req.rate is not None:
        theSimulation.rate = req.rate
    # this assignment will result in multiple functions being called
    await theSimulation.setState(req.state)
    if theSimulation.state == SimulationState.SHUTTING:
        background = BackgroundTask(shut_the_process)
    else:
        background = None
    content = SimulationResponse(
        state=theSimulation.state, rate=theSimulation.rate).model_dump()
    return JSONResponse(content=content, background=background)

async def shut_the_process():
    '''
    This is how we exit FastAPI app
    '''
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)
    print(f'{pid} shutting down...')
    return
```


### How do I programmatically add reading from a 0mq socket to the FastAPI event loop?


https://stackoverflow.com/questions/70872276/fastapi-python-how-to-run-a-thread-in-the-background

1. in the startup event handler add:
```
asyncio.create_task(self.recv_zmq_string())
```

2. define recv_zmq_string

```
    async def recv_zmq_string(self) -> str:
        res = await self._zsocket.recv_string()
        topic, message = res.split()
        assert topic == simulation_ztopic
        # dispatch message
        from pydantic import parse_obj_as
        try:
            self.on_simulation_state_update(
                parse_obj_as(SimulationResponse, json.loads(message)))
        except json.JSONDecodeError as err:
            print('recv_zmq_string caught JSONDecodeError', err)
        except Exception as err:
            print('recv_zmq_string caught Exception', err)

        return message
```

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

### Python Dependencies

..are handled using virtual environment.

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
