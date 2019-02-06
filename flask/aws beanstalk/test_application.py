# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except
# in compliance with the License. A copy of the License is located at
#
# https://aws.amazon.com/apache-2-0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"Unit tests"
import unittest.mock
import unittest
import json

####
# Mock the database methods before we import logic
####
def list_airports_mock():
    "mock the airports response"
    airports = (
        "EA100,EB100,EA200,EB200,EA101,EB101,EC101,EA201,EB201,"
        "EC201,EA102,EB102,EC102,ED102,EA202,EB202,EC202,ED102,"
        "MA50,MB50,MA100,MB100,MA51,MB51,MC51,MA101,MB101,MC101,"
        "MA52,MB52,MC52,MD52,MA102,MB102,MC102,MD102,"
        "HA50,HB50,HA60,HB60,HA51,HB51,HC51,HA61,HB61,HC61,HA52,"
        "HB52,HC52,HD52,HA62,HB62,HC62,HD62"
    )
    return [{'ident': a, 'name': 'Fake - %s' % a, 'local_code': a} for a in airports.split(',')]

def list_routes_mock():
    "mock the routes response"
    routes = [
        # easy questions - 100 miles difference
        {'route_csv': 'EA100,EB100', 'segment_count': 1, 'total_miles': 100},
        {'route_csv': 'EA200,EB200', 'segment_count': 1, 'total_miles': 200},
        {'route_csv': 'EA101,EB101,EC101', 'segment_count': 2, 'total_miles': 101},
        {'route_csv': 'EA201,EB201,EC201', 'segment_count': 2, 'total_miles': 201},
        {'route_csv': 'EA102,EB102,EC102,ED102', 'segment_count': 3, 'total_miles': 102},
        {'route_csv': 'EA202,EB202,EC202,ED102', 'segment_count': 3, 'total_miles': 202},
        # medium questions - 50 miles difference
        {'route_csv': 'MA50,MB50', 'segment_count': 1, 'total_miles': 1050},
        {'route_csv': 'MA100,MB100', 'segment_count': 1, 'total_miles': 1100},
        {'route_csv': 'MA51,MB51,MC51', 'segment_count': 2, 'total_miles': 1051},
        {'route_csv': 'MA101,MB101,MC101', 'segment_count': 2, 'total_miles': 1101},
        {'route_csv': 'MA52,MB52,MC52,MD52', 'segment_count': 3, 'total_miles': 1052},
        {'route_csv': 'MA102,MB102,MC102,MD102', 'segment_count': 3, 'total_miles': 1102},
        # hard questions - 10 miles difference
        {'route_csv': 'HA50,HB50', 'segment_count': 1, 'total_miles': 2010},
        {'route_csv': 'HA60,HB60', 'segment_count': 1, 'total_miles': 2020},
        {'route_csv': 'HA51,HB51,HC51', 'segment_count': 2, 'total_miles': 2011},
        {'route_csv': 'HA61,HB61,HC61', 'segment_count': 2, 'total_miles': 2021},
        {'route_csv': 'HA52,HB52,HC52,HD52', 'segment_count': 3, 'total_miles': 2012},
        {'route_csv': 'HA62,HB62,HC62,HD62', 'segment_count': 3, 'total_miles': 2022}
    ]
    return routes

with unittest.mock.patch('database.list_airports', list_airports_mock), \
    unittest.mock.patch('database.list_routes', list_routes_mock):
    from application import application

class ApplicationTestCase(unittest.TestCase):
    "All the Application tests"
    def setUp(self):
        application.testing = True
        self.app = application.test_client()

    def test_home(self):
        "Home route test"
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_challenge(self):
        "Challenge test"
        response = self.app.get('/api/v1.0/get_challenge')
        challenge = json.loads(response.data)
        self.assertEqual(len(challenge['easy']), 3)
        self.assertEqual(len(challenge['medium']), 3)
        self.assertEqual(len(challenge['hard']), 3)

    def test_get_route_miles(self):
        "Get miles test"
        response = self.app.post('/api/v1.0/get_route_miles',
                                 data="""{
                                      "1": { "Route": "EA100,EB100" },
                                      "2": { "Route": "EA200,EB200" }
                                    }""",
                                 content_type='application/json')
        miles = json.loads(response.data)
        self.assertEqual(miles["1"]["Miles"], 100)
        self.assertEqual(miles["2"]["Miles"], 200)

    def test_get_route_miles_bad_route(self):
        "Validation error test"
        with self.assertRaises(ValueError):
            self.app.post('/api/v1.0/get_route_miles',
                          data="""{
                              "1": { "Route": "DOESNT-EXIST" },
                              "2": { "Route": "DOESNT-EXIST" }
                            }""",
                          content_type='application/json')
