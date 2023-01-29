# #!/usr/bin/env python3
import json
import math

def calc_gcd(radius:float, latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> float:
    '''
    Description
    ----
    Calculates distance from one geolocation on a planet to another

    Args
    ----
        radius: radius of planet
        latitude_1: (km)
        longitude_1: (km)
        latitude_2: (km)
        longitude_2: (km)
    Returns
    ----
    Distance
    '''
    lat1, lon1, lat2, lon2 = map( math.radians, [latitude_1, longitude_1, latitude_2, longitude_2] )
    d_sigma = math.acos( math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(abs(lon1-lon2)))
    return ( radius * d_sigma )

def excavate(planet_radius:float, start_pos:dict, end_pos:dict, speed:float, sample_times:dict) -> float:
    '''
    Description
    -----
    Simulates a single robot expedition on a given planet from one starting
    position to an ending position where planetary materials are sampled 
    for some time.

    Args
    -----
        planet_radius: Radius(km) of planet to be explored
        start_pos: Starting site (object) for the robot
        end_pos: Ending site (object) for the robot
        speed: Maximum speed robot can travel (km/hr)
        sample_times: Dictionary which maps a given 
            composition with the time (hours) it takes to sample it.
    
    Returns
    ----
        Duration (float, hours)
        | Sample time taken (float, hours)
        | Distance travelled (float, km)

    '''
    distance = calc_gcd(planet_radius,
                        start_pos['latitude'],
                        start_pos['longitude'],
                        end_pos['latitude'],
                        end_pos['longitude'])
    sample_time = sample_times[end_pos['composition']]
    total_time = distance/speed + sample_time

    return total_time, sample_time, distance


def main():
    with open("./ml_sites.json", "r") as f:
        data = json.load(f)
        sites = data["sites"]
        distance_travelled = 0
        time_elapsed = 0
        sample_times = {"stony": 1,
                        "iron": 2, 
                        "stony-iron": 3}
        for i, site in enumerate(sites):
            duration, sample_time, distance = 0, 0, 0
            if i == 0:
                start_site = {"site_id": "start", "latitude": 16, "longitude": 82}
                duration, sample_time, distance = excavate( 3389.5,
                                                            start_site, 
                                                            site, 
                                                            10,
                                                            sample_times)
            else:
                duration, sample_time, distance, = excavate(3389.5,
                                                            sites[i-1],
                                                            site, 
                                                            10,
                                                            sample_times)
            
            print(f'Found {site["composition"]} material at site {site["site_id"]}!' + 
                     f" | Time taken: {duration:.2f} hrs" + 
                     f" | Distance travelled: {distance:.2f} km")
            distance_travelled += distance
            time_elapsed += duration + sample_time
        print(50*"=", f"\n\nExpedition Complete | {distance_travelled:.2f} km travelled in {time_elapsed:.2f} hrs")


if __name__ == "__main__":
    main()
