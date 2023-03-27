from flask import Flask, request
from typing import List
import requests
import yaml
import redis

### GLOBAL VARIABLES ###
app = Flask(__name__)
DATA_URL = "https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json"

### HELPER FUNCTIONS ###
def message_payload(msg:str, success:bool=True, stat_code=200):
    return {"message": msg, "success":success, stat_code:stat_code}
    
def get_redis_client(db:int, host:str):
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
    return redis.Redis(host=host, port=6379, db=db, decode_responses=True)

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

def get_data():
    '''
    Description
    -----------
        Returns all gene data from redis database
    Args
    -----------
        None
    Returns
    -----------
        Dictionary with all gene data from source website 
    
    '''
    global rd
    try:
        # try to return data
        return rd.hgetall("genes_data")
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
        # try to delete data
        rd.flushall()
        return True
    except Exception as err:
        # otherwise return empty list with error message
        print("Error encountered: ", err)
        return False
    
def post_data() -> None:
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

        

        # converting all key value pairs to strings
        # genes_data = {key:str(value) for key,value in genes_data.items()}

        # updating redis db
        rd.hset("genes_data", genes_data)
        return True
    except Exception as err:
        print("Excpetion caught: ", err)
        return False


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
        genes_data = get_data()
        limit = request.args.get("limit", 2**31-1)
        offset = request.args.get("offest", 0)
        if genes_data:
            return genes_data[offset:offset+limit]
        else:
            return []
    elif request.method == "POST":
        post_data()
        return message_payload("Gene Data has been posted!")
    elif request.method == "DELETE":
        status = delete_data()
        if status:
            return message_payload("Gene Data has been deleted!")
        else:
            return message_payload("An error occurred while trying to delete  data", False, 404)
    else:
        print("Data route has missed a method")
        return message_payload("Error Processing Response", False, 404)

@app.route("/genes", methods=["GET"])
def get_genes()->List[str]:
    '''
    Description
    -----------
        Assembles all hgnc_id's returns it to user
    Args
    -----------
        None
    Returns
    -----------
        list of all unique gene id's
    '''
    global rd
    try:
        limit = request.args.get("limit", 2**31-1)
        offset = request.args.get("offest", 0)

        genes_data = rd.hget("genes_data")
        gene_ids = [data.get("hgnc_id", None) for data in genes_data if data.get("hgnc_id", None) != None]

        return gene_ids[offset:limit+offset]
    except:
        print("Error retrieving genes_id data")
        return []


@app.route("/genes/<hgnc_id>", methods=["GET"])
def get_gene(hgnc_id:str)->dict:
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
        # attempt to retrieve genes_data
        genes_data = rd.hget("genes_data")
        # if genes_data exists look for specific gene
        if genes_data:
            # loop through all genes_data and search for the gene information
            # associated with the given gene id
            gene = [gene_data for gene_data in genes_data if gene_data.get(hgnc_id, None) != None]
            return gene
        else:
            return []
    except Exception as err:
        # Handles errors trying to reach redis
        print("unable to reach redis database: ", err)   

### GLOBAL VARIABLES ###
rd = get_redis_client(0, "127.0.0.1")

if __name__ == "__main__":
    # if debug key not found, default to True
    debug = get_config().get("debug", True)
    app.run(debug=debug, host="0.0.0.0")
