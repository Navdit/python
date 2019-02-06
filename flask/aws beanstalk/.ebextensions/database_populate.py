#!/usr/bin/env python3
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
""" Script to create DDL"""
import mysql.connector
import sys
import csv
import os

def populate():
    password = os.environ['PASSWORD']
    conn = mysql.connector.connect(user="root",
                                  host="localhost",
                                  database="routes",
                                  password=password)
    cursor = conn.cursor()

    airports_csv =  os.path.join(os.path.dirname(__file__), 'airport-codes.csv')

    # check if airports is populated
    cursor.execute("SELECT 1 FROM airport")
    result = cursor.fetchall()
    if not result:
        print("Populating airport")
        with open(airports_csv,'r') as csvfile: 
            reader = csv.DictReader(csvfile)
            airports = [airport for airport in reader]
            for airport in airports:
                sql = """
                INSERT INTO `airport` (ident,type,name,latitude,longitude,elevation_ft,continent,iso_country,iso_region,municipality,gps_code,iata_code,local_code)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); 
                """
    
                try:
                    cursor.execute(sql, ( airport["ident"], airport["type"], airport["name"], airport["latitude_deg"], airport["longitude_deg"], airport["elevation_ft"], airport["continent"], airport["iso_country"], airport["iso_region"], airport["municipality"], airport["gps_code"], airport["iata_code"], airport["local_code"]  ))
                    conn.commit()
                except:
                    print("Unexpected error! ", sys.exc_info())
                    sys.exit("Error!")
    else:
        print("airport already populated")

    # check if route_miles is populated
    cursor.execute("SELECT 1 FROM route_miles")
    result = cursor.fetchall()
    if not result:
        print("Populating route_miles")
        routes_csv =  os.path.join(os.path.dirname(__file__), 'routes.csv')
        with open(routes_csv,'r') as csvfile: 
            reader = csv.DictReader(csvfile)
            routes = [route for route in reader]
            for route in routes:
    
                sql = """
                INSERT INTO `route_miles` (route_csv,segment_count,direct_miles,total_miles)
                VALUES (%s,%s,%s,%s); 
                """
    
                try:
                    cursor.execute(sql, ( route["route_csv"], route["segment_count"], route["direct_miles"], route["total_miles"]  ))
                    conn.commit()
                except:
                    print("Unexpected error! ", sys.exc_info())
                    sys.exit("Error!")
    else:
        print("route_miles already populated")

    conn.close()
    


populate()
