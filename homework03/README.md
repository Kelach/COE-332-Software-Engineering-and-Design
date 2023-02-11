# Mars Turbiditiy Analyses

This project is designed to assess the quality of water in the Mars laboratory where the meteorite samples are analyzed. By checking the latest water quality data, the program will determine if it is safe to proceed with the analysis or if a boil water notice should be issued.

## Getting Started
These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Make sure you have Python3 (this project was built with Python 3.8) and pytest installed on your machine. You can install pytest by running the following command:

```
pip install pytest
```

### Accessing the Data Set

The data set used for this project can be accessed at the following link: https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json.

### Scripts

  - [analyze_water.py](./analyze_water.py): This script reads in the water quality data set "collected by the robot" and prints three key pieces of information to the screen:
          
      1. The current water turbidity (taken as the average of the most recent five data points).
      2. Whether that [turbidity](## "Turbidity is the measure of relative clarity of a liquid") is below a safe threshold
      3. The minimum time required for [turbidity](## "Turbidity is the measure of relative clarity of a liquid") to fall below the safe threshold.

  - [test_analyze_water.py](./test_analyze_water.py): This script contains unit tests for each function in analyze_water.py. Namely, the `calc_turbidity()`, `turbidity_waitime`, and `avg_turbidity`. The tester script checks the calculations made by each function using assert keywords after calling each function with a simple and hard-coded parameters.

### Running the Code
To run the water quality monitoring script, navigate to the directory where the analyze_water.py file is located and run the following command:

```
python analyze_water.py
```
 **Example output:**

```
Average turbidity based on most recent five measurements = 0.6820
INFO:root: Turbidity is below threshold for safe use
Minimum time required to return below a safe threshold = 0.00 hours
```

To run the unit tests, navigate to the directory where the test_analyze_water.py file is located and run the following command:

```
pytest test_analyze_water.py
```

**Example output:**
```
========================================== test session starts ===========================================
platform win32 -- Python 3.8, pytest-7.2.1, pluggy-1.0.0
rootdir: C:\path\to\script\directory
collected 3 items

test_analyze_water.py ...                                                                           [100%] 

=========================================== 3 passed in 0.14s ============================================
```

## Built With
  - Python3 - The programming language used
  - Pytest - The testing framework used
