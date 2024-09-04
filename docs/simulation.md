# Simulation

## Simulation State

* Init
* Initializing
* Running - maybe at a rate != 1
* Paused
* Shutting

## Simultons

Simulation spawns [simulton](simulton.md)s and eventually shuts them down.

Simulation informs simultons about:

* simulation state, e.g. whether it is paused or is running;
* simulation rate, e.g. 1:1 or 100:1

## REST service /api/v1/simulation

* GET -> SimulationResponse
* PUT, SimulationRequest -> SimulationResponse

## REST service /api/v1/simultons

* GET -> Dict[int port, SimultonResponse])
* PORT NewSimultonParams -> SimultonResponse
* GET '/api/v1/simultons/{id}' -> SimultonResponse