#!/usr/bin/python

import sys
from metrotransit_route_api import NextRide

if __name__ == "__main__":
    nr = NextRide()
    desired_route = nr.get_route(sys.argv[1])
    desired_direction = nr.validate_direction(sys.argv[3])
    desired_stop = nr.get_stop(sys.argv[2], desired_route, desired_direction)
    departure_time = nr.get_departure_time(desired_route, desired_direction, desired_stop)
    parsed_departure_time = nr.parse_departure_time(departure_time)
    next_departure_minutes = nr.minutes_until_next_departure(parsed_departure_time)
    # It always rubs me the wrong way when there's "1 minutes"
    if int(next_departure_minutes) == 1:
        print "{} Minute".format(next_departure_minutes.lstrip("0"))
    elif int(next_departure_minutes) > 1:
        print "{} Minutes".format(next_departure_minutes.lstrip("0"))
