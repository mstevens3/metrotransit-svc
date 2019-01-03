import unittest
import datetime
from metrotransit_route_api import NextRide

class TestNextRide(unittest.TestCase):
    def test_validate_direction(self):
        """
        Test validate_direction function from NextRide.
        Given the string 'North', the function should return
        a value of 4 for use in the API
        """
        requested_direction = "North"
        expected_direction_result = 4
        test_nr = NextRide()
        result = test_nr.validate_direction(requested_direction)
        self.assertEqual(result, expected_direction_result)
    def test_parse_departure_time(self):
        """
        Test parse_departure_time function from NextRide.
        Given the sample date string returned from the API, the
        function should properly extract and convert the timestamp
        """
        test_api_date = "/Date(1546448700000-0600)/"
        expected_parsed_result = datetime.datetime.fromtimestamp(1546448700.0)
        test_nr = NextRide()
        result = test_nr.parse_departure_time(test_api_date)
        self.assertEqual(result, expected_parsed_result)
    def test_minutes_until_next_departure(self):
        """
        Test minutes_until_next_departure function from NextRide.
        Given the example departure timestamp, the function should
        return a valid, inclusive value of minutes between 0 and 59
        """
        test_departure_time = datetime.datetime.fromtimestamp(1546448700.0)
        test_nr = NextRide()
        result = test_nr.minutes_until_next_departure(test_departure_time)
        self.assertTrue(int(result) >= 0 and int(result) < 60)
        


if __name__ == '__main__':
    unittest.main()
