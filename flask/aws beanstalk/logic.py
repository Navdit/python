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
"Central business logic"
import random

import database

answers_dict = {
    1: {
        "easy" : {},
        "medium" : {},
        "hard" : {}
    },
    2: {
        "easy" : {},
        "medium" : {},
        "hard" : {}
    },
    3: {
        "easy" : {},
        "medium" : {},
        "hard" : {}
    }
}
all_routes = database.list_routes()
all_airports = database.list_airports()
airport_dict = {
    airport["local_code"] : {"name" : (airport['name'])}
    for airport in all_airports
}

# populate a data structure for easy/medium/hard questions
for segs in [1, 2, 3]:
    seg_routes = [r for r in all_routes if r['segment_count'] == segs]
    for route in seg_routes:
        easy_range = (int(route['total_miles']) + 100, int(route['total_miles']) + 200)
        med_range = (int(route['total_miles']) + 50, int(route['total_miles']) + 100)
        hard_range = (int(route['total_miles']) + 10, int(route['total_miles']) + 50)
        easy_match = [p for p in seg_routes
                      if easy_range[0] <= int(p['total_miles']) <= easy_range[1]]
        med_match = [p for p in seg_routes
                     if med_range[0] <= int(p['total_miles']) < med_range[1]]
        hard_match = [p for p in seg_routes
                      if hard_range[0] <= int(p['total_miles']) < hard_range[1]]

        if easy_match:
            answers_dict[segs]["easy"][route['route_csv']] = [m['route_csv']
                                                              for m in easy_match]
        if med_match:
            answers_dict[segs]["medium"][route['route_csv']] = [m['route_csv']
                                                                for m in med_match]
        if hard_match:
            answers_dict[segs]["hard"][route['route_csv']] = [m['route_csv']
                                                              for m in hard_match]

def get_route_miles(route_csv):
    "Find total miles for a given route"
    routes = [r for r in all_routes if r['route_csv'] == route_csv]
    if not routes:
        raise ValueError("Not a valid route")
    return int(routes[0]['total_miles'])

def get_challenge():
    "Returns the challenge for a single game"
    challenges = {
        "easy" :[],
        "medium" :[],
        "hard" :[]
    }

    for difficulty in challenges:
        for segments in [1, 2, 3]:
            answers = answers_dict[segments][difficulty]
            correct_csv = random.choice(list(answers.keys()))
            correct_answer = {}
            correct_answer['route_csv'] = correct_csv
            correct_answer['airports'] = route_csv_to_airports(correct_csv)
            correct_answer['image'] = route_csv_to_image(correct_csv)
            wrong_csv = random.choice(answers[correct_csv])
            wrong_answer = {}
            wrong_answer['route_csv'] = wrong_csv
            wrong_answer['airports'] = route_csv_to_airports(wrong_csv)
            wrong_answer['image'] = route_csv_to_image(wrong_csv)

            challenge = [correct_answer, wrong_answer]
            random.shuffle(challenge)
            challenges[difficulty].append(challenge)
    return challenges

def route_csv_to_airports(route_csv):
    "Find airports by route csv"
    airports = [airport_dict[route]['name'] for route in route_csv.split(",")]
    return airports

def route_csv_to_image(route_csv):
    "Create image url for route csv"
    image = ("https://us-west-2-tcdev.s3.amazonaws.com/"
             "courses/AWS-100-ADD/v1.0.0/data/maps/%s.png") % route_csv.replace(",", "_")
    return image
