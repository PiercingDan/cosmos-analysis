for name in balogh_data1_match:
    badcount=0
    for d2d in balogh_data1_match[name][0][1]:
        if d2d >= 1.0*u.arcsec:
            badcount+=1
    print (name + " has ", badcount, " erroneous matches") 