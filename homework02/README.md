
## Meteorite Landings Investigation using "json" and "random" python libraries
Simulates a land rover excavation on mars with an informative output

## Scripts

### [generate_sites.py](./generate_sites.py):
  
  Generates 5 random meteorite landing sites using "random" python library. Sites are serialized as json objects into a json file titled [ml_sites](./ml_sites). The geolocation of the randomly generated sites were set based on the assignment requirements

### [calculate_trip.py](./calculate_trip):
  
  Conducts a single robot expedition through ever meteorite landing site on [ml_sites](./ml_sites) with informative ouputs (such as total distance travelled).


## Try it Yourself!

1.  Clone this repo
2.  Run generate_sites.py (assuming you know how to run a python file, if you don't see [this](https://www.knowledgehut.com/blog/programming/run-python-scripts)
    - Note: a new ml_sites.json will be created inside your cloned repo

3.  Run calculate_trip.py and view the status of your expedition!
    - Note: Both functions do not accept input from user.
