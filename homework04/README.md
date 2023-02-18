# International Space Station Flask App

## Project Objective

This Flask application allows the user to query [International Space Station](https://en.wikipedia.org/wiki/International_Space_Station) (ISS) positional and velocity data. The data set contains an abundance of interesting positional and velocity data for the ISS, and it can be challenging to sift through the data manually to find what you are looking for. With this application, you can easily query the ISS data set and receive interesting information.

## Data Set

- ### Access
  The ISS positional and velocity data set can be accessed from [ISS Trajectory Data Webiste (https://spotthestation.nasa.gov/trajectory_data.cfm). 

- ### Description
  The data set includes a header with additional information about the ISS like its mass (kg) and drag coefficient (m^2). 
  
  After the header, ISS state vectors, in the **Mean of J2000 (J2K) reference frame** are listed at four-minute intervals spanning a total length of 15 days. In case you're wondering, ISS state vectors in the Mean of J2000 (J2K) reference frame basically means positional and velocity values calculated for the ISS are relative to the Earth's equator and equinox.  
  
  Each state vector includes a time (epoch in Coordinated Universal Time), position vectors X, Y, and Z (km), and velcoty vectors X, Y, and Z (km/s).


## Script
- ### *[iss_tracker.py](./iss_tracker.py)*
  - Flask Application that parses and returns to the end user information about the ISS such as its position as velocity. This flask application relies on the text file format version provided by [ISS Trajectory Data Webiste (https://spotthestation.nasa.gov/trajectory_data.cfm). 
  - To view the currently support routes, see the [Running the App](#running-the-app) section
  
## Getting Started 
These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Make sure you have Python3 (this project was built with Python 3.8) and flask installed on your machine. You can install flask by running the following command:

```
pip install flask
```

## Running the App
To run the app, you will need to follow these steps:

  1. Clone this repository to your local machine.
  2. In your command terminal cd into this repository by running: `cd /path/to/coe-322-sp23/homework04`. Where you replace "/path/to/coe-322-sp23/homework04" with the path to this directory. 
  3. Start the Flask server by running: 
    `flask --app iss_tracker`.   
    
      - If you'd like to run this application in debug mode you can run this command to start the flask app instead:
      `flask --app iss_tracker --debug run`
  
  4. Lastly, Navigate to http://localhost:5000/ in your web browser to access the application and you're all set!
### Routes
  Here are the currently supported routes and query parameters:
  | Route | Returned Data
  |-------|------------------|
  | `/` | The entire data set (list of dictionaries)  <br><em> - Includes optional parameter "limit" (int) to truncate results </em></br> See [examples](#example-queries-and-results) below |
  | `/epochs` | All Epochs in the data set (list of strings) <br><em> - Includes optional parameter "limit" (int) to truncate results </em></br> See [examples](#example-queries-and-results) below |
  | `/epochs/<epoch>` | State vectors for a specific Epoch from the data set (list of one dictionary) <br> <b> < epoch > </b> Takes string inputs only.</br> See [examples](#example-queries-and-results) below |
  | `/epochs/<epoch>/speed`| Instantaneous speed for a specific Epoch in the data set (string) |
  
  
## Example Queries and Results
  - Note: you may need to add quotes ("") surrounding your epoch queries if you are using a terminal to make requests. 
    - e.g. `http://localhost:5000/epochs/"2023-02-15T12:16:00.000"`
    instead of: `http://localhost:5000/epochs/2023-02-15T12:16:00.000`

<table>
<tr>
<td> 

### Route 

</td>
<td> 

### Returned Data

</td>
</tr>
<tr>
<td> 

`http://localhost:5000?limit=3` 

</td>
<td>
    
```json
[
  {
    "X": "-4788.368507507620",
    "X_Dot": "-4.47317640532645",
    "Y": "1403.549622371260",
    "Y_Dot": "-5.44388258946684",
    "Z": "-4613.109479300690",
    "Z_Dot": "2.99705738521092",
    "epoch": "2023-02-15T12:00:00.000"
  },
  {
    "X": "-5675.021705065900",
    "X_Dot": "-2.87004030254429",
    "Y": "61.910987386751",
    "Y_Dot": "-5.66832649751615",
    "Z": "-3734.576449237840",
    "Z_Dot": "4.27967238757376",
    "epoch": "2023-02-15T12:04:00.000"
  },
  {
    "X": "-6148.993248504040",
    "X_Dot": "-1.05503300582525",
    "Y": "-1284.195507156520",
    "Y_Dot": "-5.48063337615216",
    "Z": "-2583.725124493340",
    "Z_Dot": "5.25228914094105",
    "epoch": "2023-02-15T12:08:00.000"
  }
]

```

</td>
</tr>
<tr>
<td>

`http://localhost:5000/epochs?limit=5` 

</td>
<td>
    
```json
[
  "2023-02-15T12:00:00.000",
  "2023-02-15T12:04:00.000",
  "2023-02-15T12:08:00.000",
  "2023-02-15T12:12:00.000",
  "2023-02-15T12:16:00.000"
]
```

</td>
</tr>

<tr>
<td> 

`http://localhost:5000/epochs/2023-02-15T12:16:00.000`

</td>
<td>

```json
[
  {
    "X": "-5750.560812798620",
    "X_Dot": "2.67584228156696",
    "Y": "-3604.169888126130",
    "Y_Dot": "-3.94766617813937",
    "Z": "186.445271666768",
    "Z_Dot": "6.00579498886775",
    "epoch": "2023-02-15T12:16:00.000"
  }
]

```

</td>
</tr>
<tr>
<td>

`http://localhost:5000/epochs/2023-02-15T12:16:00.000/speed`

</td>
<td>

` 'speed: 7.669 km/s' `

</td>
</tr>
</table>
