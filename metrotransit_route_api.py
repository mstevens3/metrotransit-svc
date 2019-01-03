import urllib2
from urlparse import urljoin
import json
import logging
import datetime
import sys

class NextRide:
    def __init__(self):
        """
        Initialize the class and set the base string for interactions
        with the API endpoint
        """
        self.api_endpoint = "http://svc.metrotransit.org/NexTrip/"
    def validate_direction(self, desired_direction):
        """
        Returns a numeric value for the given, case-insensitve cardinal
        direction string value
        """
        valid_directions = {"south": 1,
                            "east": 2,
                            "west": 3,
                            "north": 4}
        if desired_direction.lower() not in valid_directions.keys():
            logging.fatal("The requested direction of {} could NOT be validated!".format(desired_direction))
            sys.exit(1)
        return valid_directions[desired_direction.lower()]
    def get_api_response(self, api_request_operation_path):
        """
        Base utility function for making API requests and returning their
        results from the given path
        """
        json_route_url = urljoin(self.api_endpoint, api_request_operation_path.lstrip("/"))
        api_resp = urllib2.urlopen(json_route_url)
        json_result = json.load(api_resp)
        return json_result
    def parse_departure_time(self, departure_time_result):
        """
        Parses the given date string format returned by the API for the valid
        millisecond-accurate timestamp, converts to a seconds-based UNIX
        timestamp and returns the datetime result
        """
        parsed_time = float(str(departure_time_result).split("Date(")[1].split("-")[0]) / 1e3
        return datetime.datetime.fromtimestamp(parsed_time)
    def minutes_until_next_departure(self, parsed_departure_time):
        """
        Calculates the time difference between the given departure time in a
        datetime format and the current time, blindly assuming the departure time
        is less than an hour from now in the future
        """
        minutes_remaining = str(parsed_departure_time - datetime.datetime.now()).split(":")[1]
        return minutes_remaining
    def get_route(self, desired_route):
        """
        Given a full or partial route description, attempts to return a
        single, valid route ID for use with other API interactions
        """
        api_request_path = "Routes?format=json"
        json_route_results = self.get_api_response(api_request_path)
        clean_desired_route = str(desired_route).strip()
        filtered_results = []
        for route in json_route_results:
            if clean_desired_route in route["Description"]:
                filtered_results.append(route)
        if len(filtered_results) < 1:
            logging.fatal("No valid route results returned! Please provide a valid route name [provided: {}".format(desired_route))
        if len(filtered_results) > 1:
            logging.fatal("Too many route results returned! Please provide a more verbose route name [provided: {}]".format(desired_route))
            sys.exit(1)
        return filtered_results[0]["Route"]
    def get_stop(self, desired_stop, desired_route, desired_direction):
        """
        Given a full or partial stop description, route ID value and numeric
        direction value, returns the first (soonest/next) of the time-sorted results
        """
        api_request_path = "Stops/{}/{}?format=json".format(desired_route, desired_direction)
        json_stop_results = self.get_api_response(api_request_path)
        clean_desired_stop = str(desired_stop).strip()
        filtered_results = []
        for stop in json_stop_results:
            if clean_desired_stop in stop["Text"]:
                filtered_results.append(stop)
            elif clean_desired_stop in stop["Value"]:
                filtered_results.append(stop)
        if len(filtered_results) < 1:
            logging.fatal("No valid stop results returned! Please provide a valid stop name [provided: {}".format(desired_stop))
        if len(filtered_results) > 1:
            logging.fatal("Too many stop results returned! Please provide a more verbose stop name [provided: {}]".format(desired_stop))
            sys.exit(1)
        return filtered_results[0]["Value"]
    def get_departure_time(self, desired_route, desired_direction, desired_stop):
        """
        Given the route ID, numeric direction value and stop value, returns
        the currently scheduled departure time
        """
        api_request_path = "{}/{}/{}?format=json".format(desired_route, desired_direction, desired_stop)
        json_departure_results = self.get_api_response(api_request_path)
        if len(json_departure_results) < 1:
            sys.exit(1)
        return json_departure_results[0]["DepartureTime"]