import unittest
from fastapi.testclient import TestClient

from simultons import NewElevatorParams, ElevatorResponse
from simultons.elevator import app

client = TestClient(app)

elevators_uri = '/api/v1/elevators/'


class TestElevatorSimultonWithTestClient(unittest.TestCase):
    '''
    Verify ElevatorSimulton functionality using TestClient
    '''

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_all(self):
        '''
        Test Elevator REST APIs functionality
        '''
        #
        # blank slate, no elevators created yet
        #
        response = client.get(elevators_uri)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.json(), {})

        #
        # Create some elevators
        #
        floors = 10
        names = ['foo', 'bar', 'baz']
        for name in names:
            params = NewElevatorParams(name=name, floors=floors)
            print('posting:', params.model_dump())
            response = client.post(elevators_uri, json=params.model_dump())
            self.assertTrue(response.status_code, 201)
            jresp = response.json()
            self.assertEqual(jresp['name'], name)
        #
        # retrieve them all
        #
        response = client.get(elevators_uri)
        self.assertTrue(response.status_code, 200)
        jresp = response.json()
        #
        # retrieve them, one at a time
        #
        for id, el in jresp.items():
            response = client.get(f'{elevators_uri}{id}')
            expected = ElevatorResponse(
                id=id, name=el['name'], floors=floors)
            print('received:', response.json())
            print('expected:', expected.model_dump())
            self.assertEqual(response.json(), expected.model_dump())

        return
