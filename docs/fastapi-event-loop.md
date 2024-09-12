# How do I programmatically add reading from a 0mq socket to the FastAPI event loop?


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
