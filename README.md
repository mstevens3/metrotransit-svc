# metrotransit-svc
### A program which will tell you how long it is until the next bus on “BUS ROUTE” leaving from “BUS STOP NAME” going “DIRECTION” using the api defined at http://svc.metrotransit.org/

This program was developed using python `2.7.10`, though any standard installation of at least `2.7` _should_ work just fine. There should also not be any external dependencies as only the standard library is being utilized.

# Running the program:
1. Ensure you have a proper `python` interpreter available, which should hopefully return a version number of something like `2.7.x`:

    ```$(which python) --version```

2. Clone the repository to pull it down to your local machine:

    ```git clone https://github.com/mstevens3/metrotransit-svc.git```

3. Move into the cloned repository directory:

   ```cd metrotransit-svc```

4. Run the main program, `nextride.py` and give it three positional arguments `BUS_ROUTE` `BUS_STOP_NAME` `DIRECTION`:

    ```python ./nextride.py "METRO Blue Line" "Target Field Station Platform 1" "south"```

The values given for `BUS_ROUTE` and `BUS_STOP_NAME` can be full or partial case-sensitive names, though if no single match is found, an error will be thrown. `DIRECTION` is case-insensitive and must be a full value for any of the four primary cardinal directions `(North, South, East, West)`.

# Development:
`metrotransit_route_api.py` defines the `NextRoute` class which is utilized by `nextride.py` and can therefore be reviewed as an example of `NextRoute`'s use.

# Unit tests:
`test.py` contains a small set of unit tests which primarily focus on the `NextRoute` supporting functions which are used to manipulate the results returned from the API calls. These unit tests utlize the standard `unittest` library and can be run with the following:

```python ./test.py```
