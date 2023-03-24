# Human Genome API using Flask + Redis

## Project Objective

Easily query and modify information on the whereabouts of the [International Space Station](https://en.wikipedia.org/wiki/International_Space_Station) using the International Space Station Web API! This Flask application supports querying positional, velocity, and locational data about the ISS. The ISS API serves as an intermediary between the [ISS Trajectory Data Webiste](https://spotthestation.nasa.gov/trajectory_data.cfm) and the end user. The ISS trajectory data set contains an abundance of measuring data about the ISS, and it can be challenging to sift through the data manually to find what you are looking for. With this application, you can easily query and parse information regarding the trajectory of the ISS.

## Data Set

- ### Access
  The ISS positional and velocity data set can be accessed from the [ISS Trajectory Data Webiste](https://spotthestation.nasa.gov/trajectory_data.cfm). 

- ### Description
  The data set includes a header, metadata, and comments which include additional information about the ISS like its mass (kg) and drag coefficient (m^2). 
  
  After the additional information, ISS state vectors in the **Mean of J2000 (J2K) reference frame** are listed at four-minute intervals spanning a total length of 15 days. 
    
    - In case you're wondering, having ISS state vectors in the Mean of J2000 (J2K) reference frame essentially means the positional and velocity values calculated for the ISS are relative to the Earth's equator and equinox.  
  
  Each state vector includes an epoch (time in Coordinated Universal Time), position vectors X, Y, and Z (km), and velocity vectors X_Dot, Y_Dot, and Z_Dot (km/s).
    - Note: You can switch to USCS units (mi/s) if you wish to instead. (see [routes](#routes) for more info)


## Script
- ### *[gene_api.py](./gene_api.py)*
  - Flask Application that interacts with a Redis database containing gene information from the Human Genome Organization to handle requests from an end user. The redis database is loaded with data from the [Human Gene Nomenclature Committee Data Website](https://www.genenames.org/download/archive/).
  - To view the currently supported routes, see the [Running the App](#running-the-app) section
  
## Installation 
To get a copy of the project up and running on your local machine, you have three options:

- [Install/Run via the Docker Hub](#installrun-via-the-docker-hub)

- [Install/Run via the Dockerfile](#installrun-via-the-dockerfile)

If you're wondering "what's the difference?" Here's a small description for each installation option:

- **via the Docker Hub**: 
    - Easiest installation method, but you'll need Docker installed on your local machine.([install Docker here](https://docs.docker.com/get-docker/))
- **via the Dockerfile**: 
    - Helpful if you'd rather build the Docker image locally instead of pulling it from the Docker Hub. (not reccommended if you'd like to maintain the latest version of this application). You'll also still need Docker installed.
    - Also, building the Docker image for this application yourself gives you the freedom to modify the source code of the [gene_api.py](./gene_api.py) script and even the Docker image itself!
- **via Git Clone**:
    - This method is also helpful if you'd like to modify the source code, but without using Docker to run the application. However, system differences between my computer and yours may prevent this application from running as intended on your local computer.* 
    
**NOTE**: You'll need a reliable network connection and Python3 installed to proceed with any of the three installation methods! (this application was built using Python 3.8).


## Install/Run via the Docker Hub
First, ensure you have Docker installed on your local machine. To run the app you will need to follow these steps:

  1. Pull the Redis and gene_api Docker images from the public registry by running the following commands:
      
        `gene_api image`:

         docker pull kelach/gene_api:1.0
                
        `Redis image:`

         docker pull redis:7
  
   1. Next, run the redis container in the background with the following command:
      
          docker run -d -p 6379:6379 -v $(pwd)/data:/data:rw redis:7 --save 1 1
          
        - Incase you're new to running Docker images:
            - `-d` : Runs the container in the background  
            - `-p` : Binds port 6379 on the container to the port 6379 on your local/remote computer (so the redis database can be interacted with by the flask application)
            - `-v` : Mounts the "data" volume to the container to keep the database persistnt. Click [here](https://docs.docker.com/storage/volumes/) for more info on volume mounting.
            
   1. Now that the redis database is active you can now start a gene_api container with the following command:

            docker run -it --rm -p 5000:5000 -v $(pwd)/config.yaml:/config.yaml kelach/gene_api:1.0
    
        - Incase you're new to running Docker images:
            - `-it` : Allows you to interact in your container using your terminal
            - `--rm` : removes the container after exiting the Flask application
            - `-p` : Binds port 5000 on the container to the port 5000 on your local/remote computer (so you can communicate with the flask program)
            - `v` : Mount binds the `config.yaml` volume to the container to read user configurations.
        
        - **NOTE:** The gene_api Flask application will automatically start after running this command. Moreover, the application runs in debug mode by default. To change this, set debug flag to `False`.  
      
  3. Now that the persistent Redis database and Flask application are up and running you can navigate to http://localhost:5000/ in your web browser to access the data! See [Routes](#routes) for the supported routes.

## Install/Run via the Dockerfile
  First, ensure you have Docker installed on your local machine. To build the Docker image on your local computer, see the following steps:
  
 1. Clone this repository to your local machine by the following in your command terminal:
      
          git clone https://github.com/Kelach/coe-332-sp23.git
  
 1. In your command terminal cd into this repository by running: 
      
          cd /path/to/homework06
          
    - Where you replace "/path/to/homework06/" with the path to this directory.
      
 1. Building and running the Docker image has been automated with Docker Compose. To build and run the application type the following in your terminal:

        docker-compose up -d --build flask-app

    - Incase you're new to using docker-compose:
        - `-d` : Runs the containers in the background  
        - `--build` : Builds the flask-app image before starting the container

 1. Now that your persistent Redis database and Flask application are up and running navigate to http://localhost:5000/ in your web browser to access the data and you're all set! See [Routes](#routes) for a list of the supported routes.
 

## Routes
  Here are the currently supported routes and query parameters:
  | Route | Method | Returned Data
  |-------|---------|---------|
  | `/data` | `POST` |Posts all human genome data onto database entire data set (list of dictionaries)  <br><em> - Includes optional parameters "limit" (positive int) to truncate results and "offset" (positive int) to change the starting position at which the data is returned </em></br> See [examples](#example-queries-and-results) below |
  | `/data` | `GET` | Retrieves all uhman genome data = comments from the ISS trajectory data source file |
  | `/data` | `DELETE` | Deletes all human genome data from the redis database |
  | `/genes` | `GET` | Returns a list of all human genome unique ids <br><em> - Includes optional parameters "limit" (positive int) to truncate results and "offset" (positive int) to change the starting position at which the data is returned </em></br> See [examples](#example-queries-and-results) below |
  | `/genes/<hgnc_id>` | `GET` | Returns the information associated with a given human genome id|
  
  
  
## Example Queries and Results
  - **Notes**: 
    - You may need to add quotes ("") surrounding your queries if you are using a terminal 
        - e.g. `"http://localhost:5000/genes/HGNC:5"`
        instead of: `http://localhost:5000/genes/HGNC:5`
    - Some example reponses have been truncated to conserve spacing.

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

`http://localhost:5000/data?limit=1` 

</td>
<td>
    
```json
{
 "hgnc_id": "HGNC:5",
 "symbol": "A1BG",
 "name": "alpha-1-B glycoprotein",
 "locus_group": "protein-coding gene",
 "locus_type": "gene with protein product",
 "status": "Approved",
 "location": "19q13.43",
 "location_sortable": "19q13.43",
 "alias_symbol": "",
 "alias_name": "",
 "prev_symbol": "",
 "prev_name": "",
 "...": "...",
}
```
</td>
</tr>

<tr>
<td>

`http://localhost:5000/genes` 

</td>
<td>
    
```json
[
  "Source: This file was produced by the TOPO office within FOD at JSC.",
  "Units are in kg and m^2",
  "MASS=473413.00",
  "DRAG_ARE...",
]
```

</td>
</tr>

<tr>
<td>

`http://localhost:5000/header` 

</td>
<td>
    
```json
{
  "CCSDS_OEM_VERS": "2.0",
  "CREATION_DATE": "2023-03-04T04:34:04.606",
  "ORIGINATOR": "NASA/JSC/FOD/TOPO"
}

```

</td>
</tr>

<tr>
<td>

`http://localhost:5000/metadata` 

</td>
<td>
    
```json
{
  "CENTER_NAME": "Earth",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "STA...": "...",
  "STOP_TIME": "2023-03-18T15:47:35.995",
  "TIME_SYSTEM": "UTC",
  "USEABLE_START_TIME": "2023-03-03T15:47:35.995",
  "USEABLE_STOP_TIME": "2023-03-18T15:47:35.995"
}
```

</td>
</tr>

<tr>
<td>

`http://localhost:5000/now` 

</td>
<td>
    
```json
{
  "closest_epoch": "2023-03-05T21:31:35.995",
  "delay": {
    "units": "seconds",
    "value": -219.1373794078827
  },
  "location": {
    "altitude": {
      "units": "km",
      "value": 417.53296811711516
    },
    "geolocation": "The ISS is currently above an ocean; Unable to identify geolocation.",
    "latitude": 27.488124374989283,
    "longitude": 332.82252940196554
  },
  "speed": {
    "units": "km/s",
    "value": 7.6681216522619655
  }
}
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

```json 
{
  "units": "km/s",
  "value": 7.663940629644085
}
```

</td>
</tr>

<tr>
<td>

`http://localhost:5000/epochs/2023-02-15T12:16:00.000/location` 

</td>
<td>
    
```json
{
  "altitude": {
    "units": "km",
    "value": 427.99075304730286
  },
  "geolocation": {
    "ISO3166-2-lvl4": "ID-JA",
    "country": "Indonesia",
    "country_code": "id",
    "county": "Merangin",
    "state": "Jambi"
  },
  "latitude": -1.7412612735011228,
  "longitude": 102.32887684466722
}
```

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

`http://localhost:5000/convert?units=USCS`

</td>
<td>

```json
{
  "message": "Data has been converted to USCS units!",
  "success": true
}
```
  
</td>
</tr>

<tr>
<td>

`http://localhost:5000/delete-data`

</td>
<td>

```json
{
  "message": "Data deleted!",
  "success": true
}
```

</td>
</tr>
<tr>
<td>

`http://localhost:5000/post-data`

</td>
<td>

```json
{
  "message": "Data restored!",
  "success": true
}
```

</td>
</tr>
</table>
