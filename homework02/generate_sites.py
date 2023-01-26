# #!/usr/bin/env python3
import random
import json
def generate_ml(id, lat_range:list, long_range:list, compositions:list, prec:int = 1) -> dict:
    '''
    Description
    -------
    Generates a random meterorite landing site

    Args
    -------
        id: designed site id
        lat_range: [low, high] - Inclusive range of which random lattitude value will be generated
        long_range: [low, high] - Inclusive range of which random longitude value will be generated
        compositions: list of possible meteorite compositions
        prec: specifies desired degree of precision (# of decimal places)
    
    Returns
    --------
    Dictionary with keys "lattitude", "longitude", and "composition"
    '''
    try:
        latitude = random.randint(lat_range[0]*10**prec, lat_range[1]*10**prec) / 10**prec
        longitude = random.randint(long_range[0]*10**prec, long_range[1]*10**prec) / 10**prec

    except ValueError:
        raise ValueError("generator only accepts integers")
    finally:
        composition_index = random.randint(0, len(compositions)-1)
        composition = compositions[composition_index]
        ml_site = {
            "site_id": id,
            "latitude": latitude,
            "longitude": longitude,
            "composition": composition,
        }
    return ml_site

def main():
    sites = [generate_ml(i+1, [16, 18], [82, 84], ["stony", "iron", "stony-iron"], 13) for i in range(5)]
    data = {"sites": sites}
    # exporting
    with open("./ml_sites.json", "w") as fout:
        json.dump(data, fout, indent=2)
    
if __name__ == "__main__":
    main()
