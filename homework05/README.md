# International Space Station Flask Application Part 2!

## Project Objective

This new and improved Flask application now allows the user to query **and modify** [International Space Station](https://en.wikipedia.org/wiki/International_Space_Station) (ISS) positional and velocity data. As previously, the data set contains an abundance of interesting positional and velocity data for the ISS, and it can be challenging to sift through the data manually to find what you are looking for. With this application, you can easily query the ISS data set and receive interesting information.

## Data Set

- ### Access
  The ISS positional and velocity data set can be accessed from the [ISS Trajectory Data Webiste](https://spotthestation.nasa.gov/trajectory_data.cfm). 

- ### Description
  The data set includes a header with additional information about the ISS like its mass (kg) and drag coefficient (m^2). 
  
  After the header, ISS state vectors, in the **Mean of J2000 (J2K) reference frame** are listed at four-minute intervals spanning a total length of 15 days. In case you're wondering, ISS state vectors in the Mean of J2000 (J2K) reference frame basically means the positional and velocity values calculated for the ISS are relative to the Earth's equator and equinox.  
  
  Each state vector includes a time (epoch in Coordinated Universal Time), position vectors X, Y, and Z (km), and velocity vectors X, Y, and Z (km/s).


## Script
- ### *[iss_tracker.py](./iss_tracker.py)*
  - Flask Application that parses and returns to the end user information about the ISS such as its position as velocity. This flask application relies on the text file format version provided by the [ISS Trajectory Data Webiste](https://spotthestation.nasa.gov/trajectory_data.cfm). 
  - To view the currently supported routes, see the [Running the App](#running-the-app-via-the-docker-hub) section
  
## Getting Started 
These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
You can now run this application using Docker! To do so, make sure you have the latest version of Docker install on your Laptop/PC.


### Running the App (via the Docker Hub)
To run the app, you will need to follow these steps:

  1. Pull the Docker image from the public registry by running the following command:
      
          docker pull kelach/iss_tracker:hw05
  
  2. Now, you can run a container of the image with the following command:
      
          docker run -it --rm -p 5000:5000 kelach/iss_tracker:hw05
          
        - Incase you're new to running Docker images:
            - `-it` : Allows you to interact in your container using your terminal
            - `--rm` : removes the container after exiting the Flask application
            - `-p` : Binds port 5000 on the container to the port 5000 on your local/remote computer (so you can communicate with the flask program!)
      
  3. Now that the Flask application is running you can navigate to http://localhost:5000/ in your web browser to access the data and you're all set!

### Running the App (via Dockerfile *Optional*)
  Alternatively, if you'd like to build the docker image on your local computer instead of pulling the image from the Docker Hub, see the following steps:
  
 1. Clone this repository to your local machine by the following in your command terminal:
      
          git clone https://github.com/Kelach/coe-332-sp23.git
  
 2. In your command terminal cd into this repository by running: 
      
          cd /path/to/coe-322-sp23/homework05
          
    - Where you replace "/path/to/coe-322-sp23/homework05" with the path to this directory hw5.
      
 3. Next, build the Docker image you just pulled by running this command:
    
    **Note**: Running the command below will start the Flask application automatically
    
        docker build -t kelach/iss_tracker:hw05 .
  
  4. Now, you can run a container of the image with the following command:
      
          docker run -it --rm -p 5000:5000 kelach/iss_tracker:hw05
          
        - Incase you're new to running Docker images:
            - `-it` : Allows you to interact in your container using your terminal
            - `--rm` : removes the container after exiting the Flask application
            - `-p` : Binds port 5000 on the container to the port 5000 on your local/remote computer (so you can communicate with the flask program!)
  
  5. Now that the Flask application is running you can navigate to http://localhost:5000/ in your web browser to access the data and you're all set!
   
### Routes
  Here are the currently supported routes and query parameters:
  | Route | Method | Returned Data
  |-------|---------|---------|
  | `/` | `GET` |The entire data set (list of dictionaries)  <br><em> - Includes optional parameters "limit" (positive int) to truncate results and "offset" (positive int) to change the starting position at which the data is returned </em></br> See [examples](#example-queries-and-results) below |
  | `/epochs` | `GET` | All Epochs in the data set (list of strings) <br><em> - Includes optional parameters "limit" (positive int) to truncate results and "offset" (positive int) to change the starting position at which the data is returned</em></br> See [examples](#example-queries-and-results) below |
  | `/epochs/<epoch>` | `GET` | State vectors for a specific Epoch from the data set (list of one dictionary) <br> <b> < epoch > </b> Takes string inputs only.</br> See [examples](#example-queries-and-results) below |
  | `/help` | `GET` | Help text (string; not html friendly) that briefly describes each route |
  | `/delete-data` | `DELETE` | Deletes all stored data in the application |
  | `/post-data` | `POST` | Reloads flask application with data from the ISS Data Webstei |
  
  
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
<tr>
<td>

`http://localhost:5000/help`

</td>
<td>

string text similar to the [Routes](#routes) table

</td>
</tr>
<tr>
<td>

`http://localhost:5000/delete-data`

</td>
<td>

` 'Data deleted!' `

</td>
</tr>
<tr>
<td>

`http://localhost:5000/post-data`

</td>
<td>

` 'Data Restored!' `

</td>
</tr>
</table>
