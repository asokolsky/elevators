import unittest
from fastapi.testclient import TestClient

from simultons import app, NewElevatorParams, ElevatorResponse


client = TestClient(app)

root = '/api/v1/elevators'


class TestElevatorSimulton(unittest.TestCase):
    '''
    Verify ElevatorSimulton functionality
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
        response = client.get('/')
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.json(), [])

        response = client.get(f'{root}/')
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.json(), [])

        #
        # Create some elevators
        #
        floors = 10
        names = ['foo', 'bar', 'baz']
        for id, name in enumerate(names):
            params = NewElevatorParams(name=name, floors=floors)
            print('posting:', params.model_dump())
            response = client.post(f'{root}/', json=params.model_dump())
            self.assertTrue(response.status_code, 201)
            expected = ElevatorResponse(id=id, name=name)
            print('received:', response.json())
            print('expected:', expected.model_dump())
            self.assertEqual(
                response.json(), expected.model_dump(), 'response as expected')
        #
        # retrieve them, one at a time
        #
        for id, name in enumerate(names):
            response = client.get(f'{root}/{id}')
            expected = ElevatorResponse(id=id, name=name)
            print('received:', response.json())
            print('expected:', expected.model_dump())
            self.assertEqual(
                response.json(), expected.model_dump(), 'response as expected')
        #
        # retrieve them all
        #
        response = client.get(f'{root}/')
        expected = []
        for id, name in enumerate(names):
            expected.append(ElevatorResponse(id=id, name=name).model_dump())
        print('received:', response.json())
        print('expected:', expected)
        self.assertEqual(response.json(), expected, 'response as expected')
        return
