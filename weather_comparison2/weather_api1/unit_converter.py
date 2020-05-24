import re

def dms2dd(degrees, minutes, seconds, remainder, direction):
    """convert degrees/minutes/seconds to decimal degrees"""
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'W' or direction == 'S':
        dd *= -1
    return dd;

def dd2dms(deg):
    """convert decimal degrees to degrees/minutes/seconds"""
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def parse_dms(dms):
    """uses the dms2dd function to take a retrieved geographical input and convert it to decimal degrees"""
    parts = re.split('[^\d\w]+', dms)
    lat = dms2dd(parts[0], parts[1], parts[2], parts[3], parts[4])

    return (lat)

dd = parse_dms("78°55'44.33324'N" )

print(dd)

