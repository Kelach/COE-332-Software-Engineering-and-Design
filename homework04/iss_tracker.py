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
    parse = True if start == "" else False
    # for each line, create dictionary object and append
    # to data list.
    for line in txt.split(splitlines):
        if parse and line:
            values = line.split(splitline)
            try:
                # serializes keys and values into a dictionary
                # then appends to data list
                # print(values)
                data.append({keys[i]:values[i] for i in range(len(keys))}) 
            except IndexError as e:
                print("Lengths of values and keys DO NOT MATCH!")
                raise(e)
        if line.strip() == start.strip():
            print(line.strip(), start.strip())
            parse = True
    return data

@app.route("/", methods=["GET"])
def get_data():
    # Optional Query parameter "limit" to limit the # of results 
    # return
    try:
        limit = int(request.args.get('limit', float('inf')))
    except ValueError:
        return "ERROR: limit must be an intger"
    
    keys = ["epoch", "X", "Y", "Z", "X_Dot", "Y_Dot", "Z_Dot"]
    unparsed_data = requests.get(DATA_URL).text 
    return txt_to_dict(unparsed_data, keys, "\r\n", " ", "COMMENT End sequence of events")[:limit]

@app.route("/epochs?limit=", methods=["GET"])
def get_epochs():
    data = get_data()
    return [ISS["epoch"] for ISS in data]

@app.route("/epochs/<epoch>", methods=["GET"])
def get_state_vectors(epoch):
    data = get_data()
    return data.get(epoch, "NA")

@app.route("/epochs/<epoch>/speed", methods=["GET"])
def get_speed(epoch):
    data = get_data()
    # check to make sure epoch is in data before proceeding
    if epoch not in data: 
        return "ERROR: Request made for an epoch that does not exists"
    state_vector = data.get(epoch)
    try:
        # Tries to sums up the square of values of that last three pairs
        # (we assume the last three pairs are the velocity vectors)
        speed_squared = sum([float(vector)*float(vector) for vector in state_vector.values()[-3:]])
        speed = math.sqrt(speed_squared)
        return str(speed)
    except ValueError:
        print("Error converting speed to float")
        return ""

# the next statement should usually appear at the bottom of a flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')