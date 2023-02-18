from flask import Flask, request
from typing import List
import math
import requests
app = Flask(__name__)
DATA_URL = "https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.txt"


def txt_to_dict(txt: str, keys: List[str], splitlines: str, splitline: str, start: str = "") -> List[dict]:
    '''
    Description
    -------
    Serializes a given text into list of dictionaries where each dictionary
    was a originally a single line in the text file

    Args
    -------
        txt: Test to be parsed
        keys: list of keys to be paired with each dictionary
        splitlines: delimitter used to split each line of text
        splitline: delimitter used to split the values of each line (typically just " ")
        start: *Optional* Indicates when to start parsing text string. Used to ignore header
                information. By default, program doesn't begins parsing/serialzing immediately
    
    Returns
    --------
    List of dictionaries
    '''
    data = []
    parse = start == ""
    # for each line, create dictionary object and append
    # to data list.
    for line in txt.split(splitlines):
        if parse and line:
            values = line.split(splitline)
            try:
                # serializes keys and values into a dictionary
                # then appends to data list
                data.append({keys[i]:values[i] for i in range(len(keys))}) 
            except IndexError as e:
                print("Lengths of values and keys DO NOT MATCH!")
                raise(e)
        if line.strip() == start.strip():
            parse = True
    return data

@app.route("/", methods=["GET"])
def get_data() -> List[dict]:
    '''
    Description
    -------
        Parses ISS data into a list of dictionaries using txt_to_dict(). Takes 
        optional query parameter "limit" (int) to limit the length of the list returned

    Args
    -------
        None    
    
    Returns
    --------
    List of dictionaries containing ISS state vectors
    '''
    # Optional Query parameter "limit" to limit the # of results 
    # return
    try:
        limit = int(request.args.get('limit', 2**31 - 1))
    except ValueError:
        return ("ERROR: limit must be an intger", 404)
    
    keys = ["epoch", "X", "Y", "Z", "X_Dot", "Y_Dot", "Z_Dot"]
    unparsed_data = requests.get(DATA_URL).text 
    return txt_to_dict(unparsed_data, keys, "\r\n", " ", "COMMENT End sequence of events")[:limit]

@app.route("/epochs", methods=["GET"])
def get_epochs() -> List[str]:
    '''
    Description
    -------
        Collects all epochs from each ISS state vector. Includes
        optional query parameter "limit" (int) to limit the length of the list returned

    Args
    -------
        None    
    
    Returns
    --------
    List of strings containing ISS epochs (timestamps)
    '''
    data = get_data()
    # Optional Query parameter "limit" to limit the # of results 
    # return
    try:
        limit = int(request.args.get('limit', 2**31 - 1))
    except ValueError:
        return ("ERROR: limit must be an intger", 404)
    
    return [ISS["epoch"] for ISS in data][:limit]

@app.route("/epochs/<epoch>", methods=["GET"])
def get_state_vectors(epoch) -> List[dict]:
    '''
    Description
    -------
        Retrieves the ISS state vector at a given epoch

    Args
    -------
        - <epoch>: **URL Parameter** The epoch (timestamp) at which the ISS as a given state vector
    
    Returns
    --------
        State vector for ISS at that timed epoch
    '''
    data = get_data()
    # iterate through list and only keep objects with desired epoch value
    return [ISS for ISS in data if ISS.get("epoch") == epoch]

@app.route("/epochs/<epoch>/speed", methods=["GET"])
def get_speed(epoch) -> str:
    '''
    Description
    -------
        Calculates the speed of the ISS at a given epoch (timestamp)

    Args
    -------
        - <epoch>: **URL Parameter** The epoch (timestamp) at which the ISS as a given state vector
    
    Returns
    --------
         The speed (km/s) of the ISS at a given epoch (formatted into a string)
    '''
    state_vectors = get_state_vectors(epoch)
    # check to make sure epoch is in data before proceeding
    if len(state_vectors) == 0:
        return ("ERROR: Request made for an epoch that does not exists\n", 404)
    
    velocity_vectors = [state_vectors[0]["X_Dot"], state_vectors[0]["Y_Dot"], state_vectors[0]["Z_Dot"]]
    try:
        # takes the sum of each velocity vector squared. Then returns root of that sum.
        speed_squared = sum([float(vector)*float(vector) for vector in velocity_vectors])
        speed = math.sqrt(speed_squared)
        return f"speed: {speed:.3f} km/s\n"
    except ValueError:
        return ("Error converting speed to float")

# the next statement should usually appear at the bottom of a flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
