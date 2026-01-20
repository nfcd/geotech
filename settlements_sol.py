import numpy as np

def vert_stress(bases, gammas, gw, gamma_w=9.81):
    """
    Calculate vertical stress in a soil mass 
    consisting of a number of horizontal layers.
    The ground surface is at depth 0, and the layers are
    defined by their bases' depths and gammas arrays.
    
    Input:
    bases: array of layer bases' depths in meters
    gammas: array of layer unit weights in kN/m3
    gw: groundwater level in meters
    gamma_w: unit weight of water, kN/m3
    
    Output:
    sz_total: array of total vertical stress 
    u: array of pore water pressure 
    sz_eff: array of effective vertical stress

    Notice that the output arrays have one more element 
    than the input arrays, since the stresses start at 
    the ground surface (depth = 0.0)
    """
    
    # Check if the input arrays have the same length
    if len(bases) != len(gammas):
        print("Error: The input arrays must have the same length")
        return

    # Number of layers
    n = len(bases)
    
    # Initialize arrays
    sz_total = np.zeros(n+1) # total vertical stress
    u = np.zeros(n+1) # pore water pressure
    sz_eff = np.zeros(n+1) # effective vertical stress
    
    # insert 0 at start of bases since the ground surface is at depth 0
    bases = np.insert(bases, 0, 0)
    
    # Calculate stresses
    for i in range(n):
        # total vertical stress at the base of the layer
        sz_total[i+1] = sz_total[i] + gammas[i]*(bases[i+1] - bases[i])
        # pore water pressure at the base of the layer
        if bases[i+1] > gw:
            u[i+1] = gamma_w*(bases[i+1] - gw)
        # effective vertical stress at the base of the layer      
        sz_eff[i+1] = sz_total[i+1] - u[i+1]

    return sz_total, u, sz_eff

def vert_strain(sigma_0, delta_sigma, modulus, model=1):
    """
    Calculate vertical strain in a soil mass 
    due to a change in vertical stress.
    
    Input:
    sigma_0: initial effective vertical stress (kPa)
    delta_sigma: change in effective vertical stress (kPa)
    modulus: soil modulus number
    
    Output:
    epsilon: vertical strain
    """

    # make sure model is either 1, 2, or 3
    if model not in [1, 2, 3]:
        print("Error: model must be either 1, 2, or 3")
        return
    
    # reference stress: atmospheric pressure
    sigma_ref = 100 # kPa

    # calculate vertical strain
    if model == 1:
        # elastic model, rock, morraine, OC-clay
        epsilon = delta_sigma / (modulus*sigma_ref)
    elif model == 2:
        # elasto-plastic model, sand, coarse silt
        epsilon = (2.0/modulus)*(np.sqrt((sigma_0 + delta_sigma)/sigma_ref) - np.sqrt(sigma_0/sigma_ref))
    elif model == 3:
        # plastic model, NC-clay, fine silt
        epsilon = (1.0/modulus)*np.log((sigma_0 + delta_sigma)/sigma_0)
    
    return epsilon