# Human Genome API using Flask + Redis

## Project Objective

Easily query and modify information on the whereabouts of the [International Space Station](https://en.wikipedia.org/wiki/International_Space_Station) using the International Space Station Web API! This Flask application supports querying positional, velocity, and locational data about the ISS. The ISS API serves as an intermediary between the [ISS Trajectory Data Webiste](https://spotthestation.nasa.gov/trajectory_data.cfm) and the end user. The ISS trajectory data set contains an abundance of measuring data about the ISS, and it can be challenging to sift through the data manually to find what you are looking for. With this application, you can easily query and parse information regarding the trajectory of the ISS.

## Data Set

- ### Description
  The HGNC (HUGO Gene Nomenclature Committee) dataset provides standardized names and symbols for human genes, which helps to reduce ambiguity and confusion in the scientific community. In addition to gene names and symbols, the dataset contains information on gene descriptions, aliases, chromosome locations, protein products, gene families, and orthologs. The HGNC dataset is frequently updated and freely available. 
  
- ### Access
  The gene dataset can be accessed from the [HUGO Gene Nomenclature Committee Dataset Website](https://www.genenames.org/download/archive/). This application makes a requests to the 


## Script/Configs
- ### *[gene_api.py](./gene_api.py)*
  - Flask Application that interacts with a Redis database containing HGNC gene information to handle requests from for an end user. The redis database is initially empty when this application is run for the first time. Afterwards a persistent snapshot of the database will be saved locally on your machine.
  - To view the currently supported routes, see the [Running the App](#running-the-app) section
- ### *[config.yaml](./config.yaml)*
  - Configuration file to toggle the debug mode of the Flask application.

  
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
    
**NOTE**: You'll need a reliable network connection and Python3 installed to proceed with either installation method! (this application was built using Python 3.8).


## Install/Run via the Docker Hub
First, ensure you have [Docker installed](https://docs.docker.com/engine/install/) on your local machine. To run the app you will need to follow these steps:

  1. Pull the Redis and gene_api Docker images from the Docker Hub Image Registry by running the following commands:
      
        `gene_api image`:

         docker pull kelach/gene_api:1.0
                
        `Redis image:`

         docker pull redis:7
  1. In your chosen directory, make a folder titled `data` to ensure the Redis database remains persistent after the application has closed. 
   1. Next, run the redis container in the background with the following command:
      
          docker run -d -p 6379:6379 -v /data:/data:rw redis:7 --save 1 1
          
        - In case you're new to running Docker images:
            - `-d` : Runs the container in the background  
            - `-p` : Binds port 6379 on the container to the port 6379 on your local/remote computer (so the redis database can be interacted with by the flask application)
            - `-v` : Mounts the "data" volume to the container to keep the database persistnt. Click [here](https://docs.docker.com/storage/volumes/) for more info on volume mounting.
            - `--save` : Saves redis database to local folder `data`
            
   1. Now that the redis database is active you can now start a gene_api container with the following command:

          docker run -it --rm -p 5000:5000 -v /config.yaml:/config.yaml kelach/gene_api:1.0
    
        - In case you're new to running Docker images:
            - `-it` : Allows you to interact in your container using your terminal
            - `--rm` : removes the container after exiting the Flask application
            - `-p` : Binds port 5000 on the container to the port 5000 on your local/remote computer (so you can communicate with the flask program)
            - `-v` : Mount binds the `config.yaml` volume to the container to read user configurations.
        
        - **NOTE:** The gene_api Flask application will automatically start after running this command. Moreover, the application runs in debug mode by default. To change this, set debug flag to `False` in the `config.yaml` file.  
      
  3. Now that the persistent Redis database and Flask application are up and running you can navigate to http://localhost:5000/data in your web browser to access the data! See [Routes](#routes) for the supported routes.

   - **NOTE:** an empty list will be returned if you are starting this service for the first time.

## Install/Run via the Dockerfile
  First, ensure you have Docker installed on your local machine. To build the Docker image on your local computer, see the following steps:
  
 1. Clone this repository to your local machine by the following in your command terminal:
      
          git clone https://github.com/Kelach/coe-332-sp23.git
  
 1. In your command terminal cd into this repository by running: 
      
          cd /path/to/homework06
          
    - Where you replace "/path/to/homework06/" with the path to this directory.
      
 1. Building and running the Docker image has been automated with Docker Compose. However, To build and run the application using Docker Compose, you must first change line following line in the [`gene_api.py`](./gene_api.py) script: 
        
      `From:`
      
        line 235: rd = get_redis_client(0, "127.0.0.1")
      
      `To:`
        
        line 235: rd = get_redis_client(0, "redis-db")

 1. Now, to build and run the Flask and Redis services run the following command:

        docker-compose up -d --build flask-app

    - Incase you're new to using docker-compose:
        - `-d` : Runs the containers in the background  
        - `--build` : Builds the `flask-app` image before starting the `flask-app` container

 1. Now that your persistent Redis database and Flask application are up and running navigate to http://localhost:5000/data in your web browser to access the data and you're all set! See [Routes](#routes) for a list of the supported routes. 
 
 - **NOTE:** an empty list will be returned if you are starting this service for the first time. 
 

## Routes
  Here are the currently supported routes and query parameters:
  | Route | Method | Returned Data
  |-------|---------|---------|
  | `/data` | `POST` |Posts entire HGNC dataset onto the redis database (list of dictionaries). |
  | `/data` | `GET` | Retrieves all or some human genome data  <br><em> - Includes optional parameters "limit" (positive int) to truncate results and "offset" (positive int) to change the starting position at which the data is returned </em></br> See [examples](#example-queries-and-results) below |
  | `/data` | `DELETE` | Deletes all human genome data from the redis database |
  | `/genes` | `GET` | Returns a list of all human genome unique ids <br><em> - Includes optional parameters "limit" (positive int) to truncate results and "offset" (positive int) to change the starting position at which the data is returned </em></br> See [examples](#example-queries-and-results) below |
  | `/genes/<hgnc_id>` | `GET` | Returns the information (dictionary) associated with a given human genome id|
  
  
  
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

`"http://localhost:5000/data?limit=1"` 

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

`"http://localhost:5000/genes?limit=5"` 

</td>
<td>
    
```json
[
  "HGNC:32881",
  "HGNC:26444",
  "HGNC:42265",
  "HGNC:36070",
  "HGNC:31324"
]
```

</td>
</tr>

<tr>
<td>

`"http://localhost:5000/data/HGNC:31324"` 

</td>
<td>
    
```json
{
  "_version_": "1761544714736107520",
  "agr": "HGNC:31324",
  "date_approved_reserved": "2009-03-01",
  "date_modified": "2022-11-09",
  "ensembl_gene_id": "ENSG00000213896",
  "entrez_id": "253013",
  "hgnc_id": "HGNC:31324",
  "location": "5q12.1",
  "location_sortable": "05q12.1",
  "locus_group": "pseudogene",
  "locus_type": "pseudogene",
  "name": "ribosomal protein L31 pseudogene 8",
  "pubmed_id": "19123937",
  "refseq_accession": "NG_005654",
  "status": "Approved",
  "symbol": "RPL31P8",
  "uuid": "14d51cd0-16c6-47ff-b53a-014af67f4ce2"
}
```

</td>
</tr>
</table>
