def e_from_porosity(n):
    '''
    Calculate void ratio from porosity
    '''
    e = n / (1 - n)
    return e

def porosity_from_e(e):
    '''
    Calculate porosity from void ratio
    '''
    n = e / (1 + e)
    return n

def gamma_d_from_gamma_s(gamma_s, e):
    '''
    Calculate dry unit weight from unit weight of solids and void ratio
    '''
    gamma_d = gamma_s / (1 + e)
    return gamma_d

def gamma_from_e(e, gamma_s, w):
    '''
    Calculate unit weight from void ratio,
    unit weight of solids, and water content
    '''
    gamma = gamma_s * (1 + w) / (1 + e)
    return gamma

def e_from_gamma_s(gamma_s,w,S_r,gamma_w):
    '''
    Calculate void ratio from unit weight of solids,
    water content, saturation, and unit weight of water
    '''
    e = (w * gamma_s) / (S_r * gamma_w)
    return e

def porosity_from_gamma(gamma, gamma_s, w):
    '''
    Calculate porosity from unit weight,
    unit weight of solids, and water content
    '''
    n = 1 - (gamma / (gamma_s * (1 + w)))
    return n