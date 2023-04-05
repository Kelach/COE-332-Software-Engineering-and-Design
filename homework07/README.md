# Human Genome Flask API w/ Kubernetes Clusters

## Project Objective

This Flask application is identical to the one found in [homework06](https://github.com/Kelach/coe-332-sp23/tree/main/homework06), but now it can be deployed using a Kubernetes (K8) Cluster. As mentioned previously, this Flask API uses a persistent database with Redis, and enables users to query and parse gene information from the HUGO (Human Genome Organization) Genome Nomenclature Committee Dataset. 

- **NOTE:** This application currently does not support making requests from outside of the K8 cluster. Therefore, once the application is fully deployed, you will have to "enter" into the K8 cluster environment to make queries to the Flask application. 

- ### Redis Database 

  Instead of being saved locally, the Redis database is kept persistent using a `persistent volume claim` K8 object which acts  as storage resource provided by K8 that behaves like a global file storage system for all pods that are run within the cluster. (see all the [K8 objects](#kubernetes-config-files) for more information)

- ### Docker Support
  You must have Docker installed to run this application ([install Docker here](https://docs.docker.com/get-docker/)). In addition, you must have access to the command line tool `kubectl` (running this application in a K8 cluster without `kubtctl` is very inconvenient).

## Data Set
- ### Description
  The HGNC (HUGO Gene Nomenclature Committee) dataset provides standardized names and symbols for human genes, which helps to reduce ambiguity and confusion in the scientific community. In addition to gene names and symbols, the dataset contains information on gene descriptions, aliases, chromosome locations, protein products, gene families, and orthologs. The HGNC dataset is frequently updated and freely available. 
  
- ### Access
  The gene dataset can be accessed from the [HUGO Gene Nomenclature Committee Dataset Website](https://www.genenames.org/download/archive/). 


## Script/Configs
- ### *[gene_api.py](./gene_api.py)*
  - Flask Application that interacts with a Redis database containing HGNC gene information to handle requests from for an end user. The redis database is initially empty when this application is run for the first time. Afterwards a persistent snapshot of the database will be saved locally on your machine.
  - To view the currently supported routes, see the [Running the App](#running-the-app) section
- ### *[config.yaml](./config.yaml)*
  - Configuration file to toggle the debug mode of the Flask application.

  
## Installation 
There is only one way to run this application (using K8 clusters), however you if you'd rather build the Docker image for this application yourself see [Building Docker image](#building-the-docker-image). 
- **NOTE:** You will need to have a Docker account to proceed with building the image yourself. **In addition,** Building the Docker image yourself is especially helpful if you'd like to change the configuration settings of the Flask application, or modify any of the code in the [k8_gene_api.py](./k8_gene_api.py) script.

## Building The Docker image
  First, ensure you have Docker installed on your local machine. To build the Docker image on your local computer, see the following steps:
  
 1. Clone this repository to your local machine by the following in your command terminal:
      
          git clone https://github.com/Kelach/coe-332-sp23.git
  
 1. In your command terminal cd into this repository by running: 
      
          cd /path/to/homework07
          
    - Where you replace "/path/to/homework07/" with the path to this directory.
      
 1. If you wish to modify the source code in any productive way, you can do so now. 
 1. Next, you will want to run the following command to build the Docker image with a following tag:

        docker build -t <username>/k8_gene_api:1.0

    - Where `<username>` must be replaced with a username of your choosing. Also, incase you're new to using docker-compose:
        - `-t` : sets the tag of a given image  

 1. Finally, you will need to push this image onto the Docker Hub so  it can be accessed in the K8 cluster. To push the build Docker image onto the Docker Hub, run the following command: 
 
        docker push <username>/k8_gene_api:1.0

    - **Note:** You must be logged onto a Docker account for this command to work properly. To login to Docker from your command terminal run `docker login`. 

1. Now you can get started deploying the Flask application onto the K8 cluster. However, since you've modified the tag of the Docker image for this Flask application, you will need to change a few of the K8 deployment files. (see below)

## Kubernetes Config Files
The following is a list of all the Kubernetes object files used to deploy the Flask application with database persistence:
- [`./kelechi-test-flask-deployment.yml`](./kelechi-test-flask-deployment.yml)
    - K8 Deployment object. Used to always keep two pods running Docker containers for the Flask application. (if you built the Docker image yourself, then you will need to change `line 25` of this file to the image tag of the Docker image you pushed to the Docker Hub)
- [`./kelechi-test-flask-service.yml`](./kelechi-test-flask-service.yml)
    - K8 Service object. Used to facilitate the communication to any number of **regenerated** (that is, deleted manually, and then re-created automatically by the K8 flask deployment object) pods running the Flask applicaiton. 
- [`./kelechi-test-redis-deployment.yml`](./kelechi-test-redis-deployment.yml)
    - K8 Deployment object. Used to keep one pod running the Redis database running indefinitely. Data from the Redis database is kept persistence by volume mounting a PVC (persistent volume claim) onto each pod deployed by this K8 object.
- [`./kelechi-test-redis-pvc.yml`](./kelechi-test-redis-pvc.yml)
    - K8 Persistent Volume Claim Object. Used to reserve memory resources for the entire cluster. Allows all pods to be volume mounted with additional files. 
- [`./kelechi-test-redis-service.yml`](./kelechi-test-redis-service.yml)
    - Used to facilitate the communication between the Flask application and any number of **regenerated** (that is, deleted manually, and then re-created automatically by the K8 Redis Deployment object) pods running the Redis database.
- [`./py-debug-deployment.yml`](./py-debug-deployment.yml)
    - Used to debug and interact with the Flask API. 

## Kubernetes Cluster Deployment
Before we can deploy our Flask application it's important to note that the filenames and text for all K8 configs files must not be changed (unless you are familiar with K8 object file format). If any files or change your K8 deployment may be inhibited. 

That said, to deploy the Flask application you must:

1. Navigate to your terminal and make a new directory. Then copy all the [K8 config files](#kubernetes-config-files) into it. 
1. From your terminal, CD into the directory with all the K8 config files, and run the following commands (**NOTE:** kubectl must be installed):


        kubectl apply -f kelechi-test-flask-deployment.yml

        kubectl apply -f kelechi-test-flask-service.yml

        kubectl apply -f kelechi-test-redis-pvc.yml

        kubectl apply -f kelechi-test-redis-deployment.yml

        kubectl apply -f kelechi-test-redis-service.yml

        kubectl apply -f py-debug-deployment.yml

1. Nice! the flask application is now up and running. To check run the following comamnd in your terminal:

        kubectl get pods

    - You should see an output like this:

          kelechi-test-flask-deployment-64678d6bf9-m9lt9   1/1     Running   0               37h
          kelechi-test-flask-deployment-64678d6bf9-vqzbp   1/1     Running   0               37h
          kelechi-test-pvc-deployment-c7d8bb6f8-wxxvx      1/1     Running   0               37h
          py-debug-deployment-84c7b596c6-2djn6             1/1     Running   0               4d7h

1. In the previous Flask application you made requests to `"localhost:5000"`However, instead of making requests to the "localhost:5000" we must replace "localhost" with the hostname of our flask service. The hostname for the flask serivce is `flask-service`.

1. Now, you'll need to be "inside" the K8 cluster environment to interact with the flask API. To enter the K8 cluster environment, you must run the following command:

        kubectl exec -it <unique-py-debug-deployment-pod> -- /bin/bash
    - Where you replace `<unique-py-debug-deployment-pod>` with unique name of your py-debug-deployment pod
      - e.g. From the example output above, the command would be `kubectl exec -it py-debug-deployment-84c7b596c6-2djn6 -- /bin/bash`
1. Once you have entered into the py-debug-deploymeny pod, you are now officially inside the K8 cluster environment and can now make interact with the Flask API.

    - E.g. run `curl flask-service:5000/data` to retrieve data from the Redis database. 
 
      
1. Now that you can access the Flask application from within the K8 cluster, See below for all currently supported routes.

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
