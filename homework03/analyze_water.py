import requests

def calc_turbidity(a0:float, I90:float) -> float:
    '''
    Description
    ----
    Function calculates the water turbidity from a given water sample reading

    Parameters
    ----
    a0 - Calibration constant
    I90 - Ninety degree detector current

    Returns
    ----
    Turbidity in NTU units (0 - 40)
    
    '''
    return a0 * I90


def turbidity_waitime(T0:float,T_thres:float, decay_fact:float) -> float:
    '''
    Description
    ----
    Function calculates the time needed for current turbidity
    levels to reach a desired turbidity threshold

    Parameters
    ----
    T0 - Current turbidity
    T_Thres - Turbidity threshold for safe water
    decay_fact - decay factor per hour, expressed as a decimal (e.g. 2% -> 0.02)
    
    Returns
    ----
    Time elapsed (hours) until current turbidity
    satisfies the turbidity threshold
    
    '''

    # fix this formula should, just be a single equation
    hours = 0
    while T_thres < ( cur_turb*(1-decay_fact)**hours ):
        hours += 1
    return hours

def avg_turbidity(data:list[dict], calib:str, detect_cur:str) -> float:
    '''
    Description
    ----
    Function calculates the average turbidity from a collection of data samples

    Parameters
    ----
    data - List containing data samples to include in calculation
    calib - Dictionary key associated with the calibration constant of each sample
    detect_cur - Dictionary key associated with the 90 degree detector current

    Returns
    ----
    Average turbidity from all samples in "data"
    '''
    
    average = sum(
        [turbidity(s[calib], s[detect_cur]) for s in data ] \
    ) / len(data)
    return average

def main():
    # get data using request
    turbidity_data = []

    avg_turb = avg_turbidity(turbidity_data[-5:], 'calibration_constant', 'detector_current')

    wait_time = turbidity_waitime(avg_turb, 1, 0.02)

if __name__ == "__main__":
    main()

