import numpy as np

def stress_at_corner(m, n, load):
    '''
    Compute the vertical stress at the corner of a 
    rectangular loaded area.

    Input:
    m: rectangle_width/depth_of_point
    n: rectangle_length/depth_of_point
    load: load on the rectangle in kN/m^2
    
    Output:
    vertical stress at the corner in kN/m^2
    '''
    
    # compute the terms in the equation 10.38 of Das
    term_1 = m**2 + n**2 + 1
    term_2 = 2*m*n*np.sqrt(term_1)
    term_3 = m**2 * n**2
    term_4 = term_2 / (term_1 + term_3)
    term_5 = (term_1+1) / term_1
    term_6 = np.arctan(term_2/(term_1-term_3))
    
    # term_6 should be a positive angle in radians
    if term_6 < 0.0:
        term_6 = term_6 + np.pi
    
    # compute I3
    I3 = (1/(4*np.pi))*(term_4 * term_5 + term_6)
    
    # return the vertical stress
    return load*I3
    
def stress_at_center(m, n, load):
    '''
    Compute the vertical stress at the center of a 
    rectangular loaded area.
    
    Input:
    m: rectangle_length/rectangle_width
    n: depth_of_point/(rectangle_width/2)

    Output:
    vertical stress at the center in kN/m^2
    '''
    
    # compute the terms in equation 10.43 of Das
    term_1 = 1 + m**2 + 2*n**2
    term_2 = np.sqrt(1 + m**2 + n**2)
    term_3 = (1+n**2)*(m**2+n**2)
    term_4 = np.sqrt(m**2+n**2)*np.sqrt(1+n**2)
    
    # compute I4
    I4 = (2/np.pi)*((m*n/term_2)*(term_1/term_3)+np.arcsin(m/term_4))
    
    # return the vertical stress
    return load*I4  