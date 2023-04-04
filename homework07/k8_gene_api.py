from flask import Flask, request
from typing import List
import requests
import yaml
import redis
import os

### GLOBAL VARIABLES ###
app = Flask(__name__)
DATA_URL = "https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json"

### HELPER FUNCTIONS ###
def message_payload(msg:str, success:bool=True, stat_code=200):
    return {"message": msg, "success":success, "status code":stat_code}
    
def get_redis_client(db:int, port:int, host:str):
    '''
    Description
    -----------
        Retrieves redis client for a given database
    Args
    -----------
        db - 0-indexed id of the desired redis database
        host - hostname
    Returns
    -----------
        redis client for a given redis db
    
    '''
    return redis.Redis(host=host, port=port, db=db, decode_responses=True)

def get_config() -> dict:
    '''
    Description
    -----------
        Return config settings using config.yaml file
    Args
    -----------
        None
    Returns
    -----------
        Dictionary with configurations settings
    
    '''
    default_config = {"debug": True}
    try:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Couldn't load the config file; details: {e}")
    # if we couldn't load the config file, return the default config
    return default_config

def get_data(limit:int, offset:int) -> list:
    # genes_data[offset:offset+limit]
    '''
    Description
    -----------
        Returns all gene data from redis database
    Args
    -----------
        - limit: max length (int) of returned list 
        - offset: starting index (int)
    Returns
    -----------
        list of dictionaries with gene_data based on a desired limit and offset.  
    '''
    global rd
    try:
        # retrieve only desired keys

        gene_keys = rd.keys()[offset:offset+limit]
        # return dictionaries asscoiated with desired gene_keys
        return [rd.hgetall(gene_key) for gene_key in gene_keys]
    except Exception as err:
        # otherwise return empty list with error message
        print("Error retrieving redis db: ", err)
        return []
def delete_data():
    '''
    Description
    -----------
        Removes gene data from redis database
    Args
    -----------
        None
    Returns
    -----------
        success status True or Flase
    
    '''
    global rd

    try:
        # try to delete data and return True
        rd.flushall()
        return True
    except Exception as err:
        # otherwise return false
        print("Error encountered: ", err)
        return False
    
def post_data() -> bool:
    '''
    Description
    -----------
       Puts genes data into redis database
    Args
    -----------
        None
    Returns
    -----------
        None
    '''
    global DATA_URL, rd
    try:
        # retrieving data from source
        response = requests.get(DATA_URL).json()
        genes_data = response.get("response").get("docs")

        # setting each dictionary into redis database
        for gene in genes_data:
            # re-formatting each gene dictionary
            for gene_key,gene_val in gene.items():
                if isinstance(gene_val, list):
                    # type casting each element to string
                    gene_val = [str(element) for element in gene_val]
                    # formatting values pairs from lists to strings seperated by "|"
                    gene[gene_key] = "|".join(gene_val)
                elif isinstance(gene_val, int):
                    # type casting ints to strings
                    gene[gene_key] = str(gene_val)
            # updating database
            key = gene.get('hgnc_id')
            rd.hset(key, mapping=gene)
        print("uccess")
        return (True,None)
    except redis.exceptions.DataError:
        print("invalid inputs to write into database")
        print("value: ", gene,)
    except Exception as err:
        print("Excpetion caught: ", err)
        return (False, err)


### ROUTES ###
@app.route("/data", methods=["GET", "POST", "DELETE"])
def handle_data() -> dict:
    '''
    Description
    -----------
        Handles data (either gets, posts, or deletes data)
    Args
    -----------
        None
    Returns
    -----------
        JSON reponse or Data
    '''
    # Logic to handle GET/POST/DELETE requests
    if request.method == "GET":
        # try to evaluate query parameters
        try:
            limit = int(request.args.get("limit", 2**31-1))
            offset = int(request.args.get("offset", 0))
            return get_data(limit, offset)
        except ValueError:
            # catch invalid query parameter inputs
            return (message_payload("Invalid query parameter. 'limit' and 'offset' parameters must be positive integers only", False, 504), 504)
    elif request.method == "POST":
        success, err = post_data()
        if success:
            return message_payload("Gene data has been posted")
        else:
            return (message_payload("Unable to post gene data", False, 500), 500)
    elif request.method == "DELETE":
        success = delete_data()
        if success:
            return message_payload("Gene Data has been deleted!")
        else:
            return (message_payload("An error occurred while trying to delete  data", False, 500), 500)
    else:
        return (message_payload("Error Processing Response", False, 404), 404)

@app.route("/genes", methods=["GET"])
def get_genes()->List[str]:
    '''
    Description
    -----------
        Assembles all hgnc_id's and returns it to user
    Args
    -----------
        None
    Returns
    -----------
        list of all unique gene id's
    '''
    global rd
    try:
        limit = int(request.args.get("limit", 2**31-1))
        offset = int(request.args.get("offset", 0))
        return rd.keys()[offset:limit+offset]
    except TypeError:
        # catch invalid query parameter inputs
        return (message_payload("Invalid query parameter. 'limit' and 'offset' parameters must be positive integers only", False, 504), 504)
    except Exception as err:
        print("Error retrieving genes_id data: ", err)
        return []


@app.route("/genes/<hgnc_id>", methods=["GET"])
def get_gene(hgnc_id:str) -> dict:
    '''
    Description
    -----------
        Returns all data associated with a given hgnc_id
    Args
    -----------
        hgnc_id - Unique ID associted with each gene
    Returns
    -----------
        Information (dictionary) associated with a given gene ID (hgnc_id)
    '''
    global rd
    try:
       return rd.hgetall(hgnc_id)
    except Exception as err:
        # Handles errors trying to reach redis
        print("unable to reach redis database: ", err)   

### GLOBAL VARIABLES ###  
rd = get_redis_client(0,os.getenv("redis_service_port"), os.getenv("redis_service_host"))

if __name__ == "__main__":
    # if debug key not found, default to True
    debug = get_config().get("debug", True)
    app.run(debug=debug, host="0.0.0.0")
