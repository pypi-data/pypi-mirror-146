def altura (feet,inches):
    cm1= feet * 30.48
    cm2 = inches * 2.54
    cm3 = cm1 + cm2
    m = cm3/100
    return m

def height (metros):
    ft = metros //0.3048
    resto_ft = metros % 0.3048
    inc = resto_ft//0.0254
    return [int(ft), int(inc)]

def quilometros(miles):
    km = 1.6 * miles
    return km

def miles(quilometros):
    ml = quilometros / 1.6
    return ml

def metros(yards):
    m = yards * 0.9144
    return m

def yards (metros):
    yd = metros / 0.9144
    return yd
    
