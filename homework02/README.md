
## Meteorite Landings Investigation using "json" and "random" python libraries
Simulates a land rover excavation on mars with an informative output

## Scripts

### [generate_sites.py](./generate_sites.py):
  
  Generates 5 random meteorite landing sites using "random" python library. Sites are serialized as json objects into a json file titled [ml_sites](./ml_sites). The geolocation of the randomly generated sites were bounded by a ranged per one of the requirements of this assignment.

### [calculate_trip.py](./calculate_trip):
  
  Conducts a single robot expedition through ever meteorite landing site on [ml_sites](./ml_sites) with informative ouputs (such as total distance travelled).


## Try it Yourself!

1.  Clone this repo
2.  Run generate_sites.py (assuming you know how to run a python file, if you don't see [this](https://www.knowledgehut.com/blog/programming/run-python-scripts)
    - Note: a new ml_sites.json will be created inside your cloned repo

3.  Run calculate_trip.py and view the status of your expedition!
    - Note: Both functions do not accept input from user.

## Instructions
Step 1: Clone this github repository with this command: `git clone https://github.com/Kelach/coe-332-sp23/tree/main/homework02`

Step 2: CD into the homework02 directory 

Step 3: run `python3 generate_sites.py`

Step 4: run simulation using `python3 calculate_trip.py` 

## Example Output: 
```
Found stony-iron material at site 1! | Time taken: 12.50 hrs | Distance travelled: 95.04 km
Found stony-iron material at site 2! | Time taken: 9.33 hrs | Distance travelled: 63.28 km
Found iron material at site 3! | Time taken: 9.26 hrs | Distance travelled: 72.64 km
Found stony material at site 4! | Time taken: 8.28 hrs | Distance travelled: 72.76 km
Found stony material at site 5! | Time taken: 10.56 hrs | Distance travelled: 95.59 km
==================================================

Expedition Complete | 399.31 km travelled in 49.93 hrs
```

